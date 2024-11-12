import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-pro")


st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
            max-width: 700px;
            margin: auto;
        }
        /* Header styling */
        h1 {
            color: #1f2937;
            font-weight: 600;
            text-align: center;
            font-size: 2.8rem;
        }
        h2, h3 {
            color: #374151;
        }
        /* Button styling (red background with white text) */
        .stButton button {
            color: #ffffff; /* White text */
            background-color: blue; /* Red background */
            border: none;
            border-radius: 10px; /* Rounded corners */
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3); /* Subtle shadow */
            transition: background-color 0.3s ease, color 0.3s ease; /* Smooth transition */
        }

        /* No active or hover effect */
        /* Code block styling */
        .stCodeBlock {
            background-color: #f9fafb;
            color: #1f2937;
            font-size: 0.9rem;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #2563eb;
        }
        /* Explanation Section */
        .explanation {
            padding: 1rem;
            background-color: #e0f2fe;
            border-radius: 8px;
            margin-top: 1rem;
            color: #065f46;
            border-left: 4px solid #0284c7;
        }
        /* Success Notification */
        .success {
            background-color: #d1fae5;
            color: #065f46;
            padding: 1rem;
            border-radius: 5px;
            text-align: center;
            margin-top: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)


st.title("SQL Query Generator")
st.markdown("""
    ### Transform your questions into SQL queries instantly!
    Simply enter a question in natural language, and this tool will generate the corresponding SQL query.
""")


st.header("Ask Your Question")
question = st.text_area("Enter your question", placeholder="e.g., Show me the top 10 customers by purchase amount")


if st.button("Generate SQL Query"):
    with st.spinner("Generating SQL query..."):
        # Define prompt template for generating SQL query
        template = """
            Create a SQL query snippet using the below text: 
            
            ```
            {question}
            ``` 
            I only need a SQL query and no explanation.
        """
        f_template = template.format(question=question)
        
        # Get AI-generated query
        try:
            response = model.generate_content(f_template)
            generated_query = response.text.strip()

            # Remove triple backticks if present
            generated_query = generated_query.replace("```sql", "").replace("```", "").strip()
            st.subheader("1. Generated SQL Query")
            st.code(generated_query, language="sql")

            
            input_table_prompt = f"""
                Based on the query below, create a sample input table with realistic data:
                
                ```sql
                {generated_query}
                ```
                Provide a sample table with at least 5 rows of data and ensure the data is realistic and corresponds to the columns in the query.
            """
            response_input_table = model.generate_content(input_table_prompt)
            st.subheader("2. Sample Input Table")
            st.write(response_input_table.text)

            
            output_table_prompt = f"""
                Based on the query below and the input table provided, create a sample output table:
                
                ```sql
                {generated_query}
                ```
                Make sure the data in the output table is the result of the SQL query applied to the input table.
            """
            response_output_table = model.generate_content(output_table_prompt)
            st.subheader("3. Sample Output Table")
            st.write(response_output_table.text)
            
            
            explanation_prompt = f"""
                Explain the purpose of the following SQL query in simple, clear terms:
                
                ```sql
                {generated_query}
                ```
            """
            explanation_response = model.generate_content(explanation_prompt)
            st.subheader("4. Explanation")
            st.markdown(f"""
                <div class="explanation">
                    {explanation_response.text}
                </div>
            """, unsafe_allow_html=True)

            
            st.markdown(""" 
                <div class="success">
                    ✅ SQL Query Generated Successfully!
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Failed to generate SQL query: {e}")

            
st.markdown("<div class='footer'> :-) Smile Please 🤗</div>", unsafe_allow_html=True)
