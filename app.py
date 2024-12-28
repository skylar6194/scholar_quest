from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv
import markdown2
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

# Configure Flask to serve static files from root directory
app = Flask(__name__, static_url_path='', static_folder='.')

try:
    # Configure Gemini AI
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Load the scholarship dataset
    DATASET_PATH = 'scholarship_dataset_combined.csv'
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset file not found: {DATASET_PATH}")
    
    logger.info(f"Loading dataset from {DATASET_PATH}")
    scholarships_df = pd.read_csv(DATASET_PATH)
    logger.info(f"Dataset loaded successfully with {len(scholarships_df)} rows")
    
    # Create dataset summary for context
    total_scholarships = len(scholarships_df)
    education_levels = scholarships_df['Education Qualification'].unique().tolist()
    communities = scholarships_df['Community'].unique().tolist()
    religions = scholarships_df['Religion'].unique().tolist()
    
    DATASET_SUMMARY = f"""
    Scholarship Database Summary:
    - Total Scholarships: {total_scholarships}
    - Education Levels: {', '.join(education_levels)}
    - Communities: {', '.join(communities)}
    - Religions: {', '.join(religions)}
    """
    logger.info(f"Dataset summary created: {DATASET_SUMMARY}")
    
except Exception as e:
    logger.error(f"Initialization error: {str(e)}")
    logger.error(traceback.format_exc())
    raise

def format_message(content, role):
    try:
        formatted_content = markdown2.markdown(content) if role == 'assistant' else content
        return formatted_content
    except Exception as e:
        logger.error(f"Error formatting message: {str(e)}")
        return content

def get_scholarship_stats():
    """Get statistical information about scholarships"""
    stats = {
        'total': len(scholarships_df),
        'by_education': scholarships_df['Education Qualification'].value_counts().to_dict(),
        'by_community': scholarships_df['Community'].value_counts().to_dict(),
        'by_religion': scholarships_df['Religion'].value_counts().to_dict(),
        'by_gender': scholarships_df['Gender'].value_counts().to_dict()
    }
    return stats

def find_relevant_scholarships(student_info, query=None):
    """Find scholarships matching student criteria and query"""
    try:
        logger.info(f"Finding scholarships for student info: {student_info}")
        matches = []
        
        # Base filters
        filters = []
        
        # Education level filter
        education_level = student_info.get('educationLevel', '').lower()
        if education_level:
            if 'high school' in education_level or '12' in education_level:
                filters.append(scholarships_df['Education Qualification'].str.contains('12|high school|secondary', case=False, na=False))
            elif 'undergraduate' in education_level or 'bachelor' in education_level:
                filters.append(scholarships_df['Education Qualification'].str.contains('undergraduate|bachelor|UG', case=False, na=False))
            elif 'postgraduate' in education_level or 'master' in education_level:
                filters.append(scholarships_df['Education Qualification'].str.contains('postgraduate|master|PG', case=False, na=False))

        # Community filter
        category = student_info.get('category', '').upper()
        if category:
            filters.append(scholarships_df['Community'].str.contains(category, case=False, na=False))

        # Income filter
        try:
            income = float(student_info.get('income', 0))
            scholarships_df['Income_Numeric'] = scholarships_df['Income'].apply(lambda x: float('inf') if pd.isna(x) else float(x.replace('Upto ', '').replace('L', '')) * 100000 if 'Upto' in str(x) else float('inf'))
            filters.append(scholarships_df['Income_Numeric'] >= income)
        except (ValueError, TypeError):
            logger.warning("Invalid income value, skipping income filter")

        # Percentage filter
        try:
            percentage = float(student_info.get('percentage', 0))
            scholarships_df['Min_Percentage'] = scholarships_df['Annual-Percentage'].apply(lambda x: float(str(x).split('-')[0]) if pd.notna(x) and '-' in str(x) else 0)
            filters.append(scholarships_df['Min_Percentage'] <= percentage)
        except (ValueError, TypeError):
            logger.warning("Invalid percentage value, skipping percentage filter")

        # Apply all filters
        if filters:
            filtered_df = scholarships_df[pd.concat(filters, axis=1).all(axis=1)]
        else:
            filtered_df = scholarships_df

        # If there's a specific query, try to match it
        if query:
            query = query.lower()
            query_matches = []
            
            # Search in scholarship names
            name_matches = filtered_df[filtered_df['Name'].str.lower().str.contains(query, na=False)]
            query_matches.extend(name_matches.to_dict('records'))
            
            # Search in education qualification
            edu_matches = filtered_df[filtered_df['Education Qualification'].str.lower().str.contains(query, na=False)]
            query_matches.extend(edu_matches.to_dict('records'))
            
            # Search in community
            community_matches = filtered_df[filtered_df['Community'].str.lower().str.contains(query, na=False)]
            query_matches.extend(community_matches.to_dict('records'))
            
            # Remove duplicates
            seen = set()
            matches = []
            for item in query_matches:
                item_hash = item['Name']
                if item_hash not in seen:
                    seen.add(item_hash)
                    matches.append(item)
        else:
            matches = filtered_df.to_dict('records')

        # Sort matches by relevance (you can customize this)
        matches = matches[:10]  # Limit to top 10 matches
        
        logger.info(f"Found {len(matches)} matching scholarships")
        return matches
        
    except Exception as e:
        logger.error(f"Error finding scholarships: {str(e)}")
        logger.error(traceback.format_exc())
        return []

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/submit-info', methods=['POST'])
def submit_info():
    try:
        student_info = request.json
        logger.info(f"Received student info: {student_info}")
        return jsonify({
            'status': 'success',
            'message': 'Information submitted successfully'
        })
    except Exception as e:
        logger.error(f"Error in submit_info: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        student_info = data.get('studentInfo', {})
        
        logger.info(f"Processing chat request with message: {user_message}")
        logger.debug(f"Student info: {student_info}")
        
        # Get statistics about scholarships
        stats = get_scholarship_stats()
        
        # Find matching scholarships based on both student info and user query
        matching_scholarships = find_relevant_scholarships(student_info, user_message.lower())
        
        # Create scholarship information string
        scholarship_info = "\n\nRelevant Scholarships:\n"
        for idx, scholarship in enumerate(matching_scholarships, 1):
            scholarship_info += f"""
            {idx}. {scholarship.get('Name', 'N/A')}
            - Education Level: {scholarship.get('Education Qualification', 'N/A')}
            - Community: {scholarship.get('Community', 'N/A')}
            - Required Percentage: {scholarship.get('Annual-Percentage', 'N/A')}
            - Income Criteria: {scholarship.get('Income', 'N/A')}
            - Additional Criteria:
              * Gender: {scholarship.get('Gender', 'N/A')}
              * Religion: {scholarship.get('Religion', 'N/A')}
              * Ex-servicemen: {scholarship.get('Exservice-men', 'N/A')}
              * Disability: {scholarship.get('Disability', 'N/A')}
              * Sports: {scholarship.get('Sports', 'N/A')}
            """
        
        # Create context-aware prompt
        system_prompt = f"""
        You are a helpful education counselor assistant with access to a scholarship database. Use the following information to provide relevant advice:
        
        Database Context:
        {DATASET_SUMMARY}
        
        Statistics:
        - Total Scholarships: {stats['total']}
        - Scholarships by Education Level: {stats['by_education']}
        - Scholarships by Community: {stats['by_community']}
        - Scholarships by Religion: {stats['by_religion']}
        - Scholarships by Gender: {stats['by_gender']}
        
        Student Profile:
        - Name: {student_info.get('fullName')}
        - Age: {student_info.get('age')}
        - Education: {student_info.get('educationLevel')}
        - Course: {student_info.get('course')}
        - Family Income: ₹{student_info.get('income')}
        - Category: {student_info.get('category')}
        - State: {student_info.get('state')}
        - Previous Year Percentage: {student_info.get('percentage')}%

        {scholarship_info}

        User Query: {user_message}

        Provide a detailed response that:
        1. Directly answers the user's question
        2. Highlights relevant scholarships from the matches
        3. Provides specific eligibility criteria and requirements
        4. Suggests next steps or additional opportunities
        5. Includes relevant statistics from the database

        Format your response using markdown:
        - Use ## for main sections
        - Use ** for important points
        - Use bullet points for lists
        - Highlight key numbers and dates
        """
        
        logger.debug("Generating response with Gemini")
        # Generate response using Gemini
        response = model.generate_content([
            {'role': 'user', 'parts': [system_prompt]}
        ])
        
        formatted_response = format_message(response.text, 'assistant')
        
        return jsonify({
            'status': 'success',
            'response': formatted_response
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': f"An error occurred: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)
