# import streamlit as st
# from prompt_template_database import session, PromptTemplate
# from langchain.prompts import ChatPromptTemplate

# # Function to create Streamlit input fields for string variables
# def create_input_fields(variables):
#     inputs = {}
#     for variable in variables:
#         var_name = variable
#         inputs[var_name] = st.text_input(var_name)
#     return inputs

# # Main function to run the Streamlit app
# def main():
#     st.sidebar.title('Select Action')

#     action = st.sidebar.radio('Action', ['Display Editable Template', 'Load and Display Template'])

#     if action == 'Display Editable Template':
#         st.sidebar.title('Select Prompt Template')
#         templates = session.query(PromptTemplate).all()
#         template_names = ["New Template"]  # Make "New Template" the first option
#         template_names.extend([template.name for template in templates])

#         selected_template_name = st.sidebar.selectbox('Template', template_names)

#         if selected_template_name == "New Template":
#             selected_template = None
#             st.empty()
#             name = st.text_input('Name')
#             topic = st.text_input('Topic')
#             purpose = st.text_area('Purpose')
#             template = st.text_area('Template', height=None)  # Make the text area expand vertically
#             if st.button('Save New Template'):
#                 if not topic:
#                     st.error('Please enter a topic for the template!')
#                 if not name:
#                     st.error('Please enter a name for the template!')
#                 else:
#                     if name in template_names[1:]:
#                         st.error('A template with this name already exists!')
#                     else:
#                         new_template = PromptTemplate(topic=topic, name=name, purpose=purpose, template=template)
#                         session.add(new_template)
#                         session.commit()
#                         st.success('Template saved successfully!')
#         else:
#             selected_template = session.query(PromptTemplate).filter_by(name=selected_template_name).first()
#             if selected_template:
#                 topic = st.text_input('Topic', value=selected_template.topic)
#                 name = st.text_input('Name', value=selected_template.name)
#                 purpose = st.text_area('Purpose', value=selected_template.purpose)
#                 template = st.text_area('Template', value=selected_template.template, height=None)  # Make the text area expand vertically
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button('Save', key="save_button"):
#                         if not topic:
#                             st.error('Please enter a topic for the template!')
#                         if not name:
#                             st.error('Please enter a name for the template!')
#                         else:
#                             if name != selected_template_name and name in template_names[1:]:
#                                 st.error('A template with this name already exists!')
#                             else:
#                                 selected_template.name = name
#                                 selected_template.purpose = purpose
#                                 selected_template.template = template
#                                 session.commit()
#                                 st.success('Changes saved successfully!')
#                 with col2:
#                     if st.button('Delete', key="delete_button"):
#                         if selected_template:
#                             session.delete(selected_template)
#                             session.commit()
#                             st.success('Template deleted successfully!')
#     elif action == 'Load and Display Template':
#         st.sidebar.title('Select Prompt Template')
#         templates = session.query(PromptTemplate).all()
#         template_names = [template.name for template in templates]

#         selected_template_name = st.sidebar.selectbox('Template', template_names)

#         selected_template = session.query(PromptTemplate).filter_by(name=selected_template_name).first()

#         if selected_template:
#             st.write(f"Topic: {selected_template.topic}")
#             st.write(f"Name: {selected_template.name}")
#             st.write(f"Purpose: {selected_template.purpose}")
#             st.write(f"Template: {selected_template.template}")

#              # Add a dropdown for selecting language model
#             language_model = st.selectbox('Select Language Model', ['ChatGPT', 'Local Language Model'])
#             if language_model == 'ChatGPT':
#                 pass
#             elif language_model == 'Local Language Model':
#                 # Load your local language model here
#                 pass
#             prompt_template = ChatPromptTemplate.from_template(selected_template.template)
#             input_variables = prompt_template.messages[0].prompt.input_variables
#             inputs = create_input_fields(input_variables)

#             if st.button("Submit"):
#                 input_values = {}
#                 for var_name, var_value in inputs.items():
#                     input_values[var_name] = var_value
#                 prompt = ChatPromptTemplate.from_template(selected_template.template)
#                 formatted_messages = prompt.format_messages(**input_values)
#                 st.text_area(label='Prompt', value=formatted_messages)

# if __name__ == '__main__':
#     main()

import streamlit as st
from prompt_template_database import session, PromptTemplate
from langchain.prompts import ChatPromptTemplate


# Function to create Streamlit input fields for string variables
def create_input_fields(variables):
    inputs = {}
    for variable in variables:
        var_name = variable
        inputs[var_name] = st.text_input(var_name)
    return inputs


# retrieve templates by topic from db
def get_templates():
    topics = [
        result[0] for result in session.query(PromptTemplate.topic).distinct()
    ]
    selected_topic = st.sidebar.selectbox(
        "Select Topic", ["All"] + topics
    )  # Add dropdown for selecting topic
    if selected_topic == "All":
        templates = session.query(PromptTemplate).all()
    else:
        templates = (
            session.query(PromptTemplate).filter_by(topic=selected_topic).all()
        )
    return templates


# Main function to run the Streamlit app
def main():
    st.sidebar.title("Select Action")

    action = st.sidebar.radio(
        "Action", ["Display Editable Template", "Load and Display Template", "Prompting Principles"]
    )

    if action == "Prompting Principles":
        st.markdown('''
                ### Prompting Principles

                #### Write clear and specific instructions
                #### Give the model time to “think”

                ### Tactics

                #### Use delimiters to clearly indicate distinct parts of the input

                Delimiters can be anything like: ``, """, < >, <tag> </tag>, :
                
                #### Ask for a structured output
                
                Structured output could be JSON, plantUML or HTML
                
                #### Ask the model to check whether conditions are satisfied
                
                prompt = f"""
                You will be provided with text delimited by triple quotes. 
                If it contains a sequence of instructions, \ 
                re-write those instructions in the following format:

                Step 1 - ...
                Step 2 - …
                …
                Step N - …

                If the text does not contain a sequence of instructions, \ 
                then simply write \"No steps provided.\"

                #### "Few-shot" prompting
                
                prompt = f"""
                Your task is to answer in a consistent style.

                <child>: Teach me about patience.

                <grandparent>: The river that carves the deepest \ 
                valley flows from a modest spring; the \ 
                grandest symphony originates from a single note; \ 
                the most intricate tapestry begins with a solitary thread.

                <child>: Teach me about resilience.
                """
                response = get_completion(prompt)
                print(response)
                
                ####  Specify the steps required to complete a task
                
                f"""
                Perform the following actions: 
                1 - Summarize the following text delimited by triple \
                backticks with 1 sentence.
                2 - Translate the summary into French.
                3 - List each name in the French summary.
                4 - Output a json object that contains the following \
                keys: french_summary, num_names.

                Separate your answers with line breaks.

                Text:
                ```{text}```
                """
                #### Instruct the model to work out its own solution before rushing to a conclusion
                
                f"""
                Your task is to determine if the student's solution \
                is correct or not.
                To solve the problem do the following:
                - First, work out your own solution to the problem including the final total. 
                - Then compare your solution to the student's solution \ 
                and evaluate if the student's solution is correct or not. 
                Don't decide if the student's solution is correct until 
                you have done the problem yourself.

                Use the following format:
                Question:
                ```
                question here
                ```
                Student's solution:
                ```
                student's solution here
                ```
                Actual solution:
                ```
                steps to work out the solution and your solution here
                ```
                Is the student's solution the same as actual solution \
                just calculated:
                ```
                yes or no
                ```
                Student grade:
                ```
                correct or incorrect
                ```

                Question:
                ```
                I'm building a solar power installation and I need help \
                working out the financials. 
                - Land costs $100 / square foot
                - I can buy solar panels for $250 / square foot
                - I negotiated a contract for maintenance that will cost \
                me a flat $100k per year, and an additional $10 / square \
                foot
                What is the total cost for the first year of operations \
                as a function of the number of square feet.
                ``` 
                Student's solution:
                ```
                Let x be the size of the installation in square feet.
                Costs:
                1. Land cost: 100x
                2. Solar panel cost: 250x
                3. Maintenance cost: 100,000 + 100x
                Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
                ```
                Actual solution:
                """
                ''')
        

    if action == "Display Editable Template":
        st.sidebar.title("Select Prompt Template")
        
        templates = get_templates()
        template_names = ["New Template"]  # Make "New Template" the first option
        template_names.extend([template.name for template in templates])

        selected_template_name = st.sidebar.selectbox("Template", template_names)

        if selected_template_name == "New Template":
            selected_template = None
            st.empty()            
            name = st.text_input("Name")
            topic = st.text_input("Topic")
            purpose = st.text_area("Purpose")
            template = st.text_area(
                "Template", height=250
            )  # Make the text area expand vertically
            if st.button("Save New Template"):
                if not topic:
                    st.error("Please enter a topic for the template!")
                if not name:
                    st.error("Please enter a name for the template!")
                else:
                    if name in template_names[1:]:
                        st.error("A template with this name already exists!")
                    else:
                        new_template = PromptTemplate(
                            topic=topic, name=name, purpose=purpose, template=template
                        )
                        session.add(new_template)
                        session.commit()
                        st.success("Template saved successfully!")
        else:
            selected_template = (
                session.query(PromptTemplate)
                .filter_by(name=selected_template_name)
                .first()
            )
            if selected_template:
                topic = st.text_input("Topic", value=selected_template.topic)
                name = st.text_input("Name", value=selected_template.name)
                purpose = st.text_area("Purpose", value=selected_template.purpose)
                template = st.text_area(
                    "Template", value=selected_template.template, height=400
                )  # Make the text area expand vertically
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save", key="save_button"):
                        if not topic:
                            st.error("Please enter a topic for the template!")
                        if not name:
                            st.error("Please enter a name for the template!")
                        else:
                            if (
                                name != selected_template_name
                                and name in template_names[1:]
                            ):
                                st.error("A template with this name already exists!")
                            else:
                                selected_template.name = name
                                selected_template.purpose = purpose
                                selected_template.template = template
                                session.commit()
                                st.success("Changes saved successfully!")
                with col2:
                    if st.button("Delete", key="delete_button"):
                        if selected_template:
                            session.delete(selected_template)
                            session.commit()
                            st.success("Template deleted successfully!")
    elif action == "Load and Display Template":
        st.sidebar.title("Select Prompt Template")
        templates = get_templates()
        template_names = [template.name for template in templates]

        selected_template_name = st.sidebar.selectbox("Template", template_names)

        selected_template = (
            session.query(PromptTemplate).filter_by(name=selected_template_name).first()
        )

        if selected_template:
            st.write(f"Topic: {selected_template.topic}")
            st.write(f"Name: {selected_template.name}")
            st.write(f"Purpose: {selected_template.purpose}")
            st.write(f"Template: {selected_template.template}")

            # Add a dropdown for selecting language model
            language_model = st.selectbox(
                "Select Language Model", ["ChatGPT", "Local Language Model"]
            )
            if language_model == "ChatGPT":
                pass
            elif language_model == "Local Language Model":
                # Load your local language model here
                pass
            prompt_template = ChatPromptTemplate.from_template(
                selected_template.template
            )
            input_variables = prompt_template.messages[0].prompt.input_variables
            inputs = create_input_fields(input_variables)

            if st.button("Submit"):
                input_values = {}
                for var_name, var_value in inputs.items():
                    input_values[var_name] = var_value
                prompt = ChatPromptTemplate.from_template(selected_template.template)
                formatted_messages = prompt.format_messages(**input_values)
                st.text_area(label="Prompt", value=formatted_messages,height=500)


if __name__ == "__main__":
    main()
