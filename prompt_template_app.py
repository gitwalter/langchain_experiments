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
#             purpose = st.text_area('Purpose')
#             template = st.text_area('Template', height=None)  # Make the text area expand vertically
#             if st.button('Save New Template'):
#                 if not name:
#                     st.error('Please enter a name for the template!')
#                 else:
#                     if name in template_names[1:]:
#                         st.error('A template with this name already exists!')
#                     else:
#                         new_template = PromptTemplate(name=name, purpose=purpose, template=template)
#                         session.add(new_template)
#                         session.commit()
#                         st.success('Template saved successfully!')
#         else:
#             selected_template = session.query(PromptTemplate).filter_by(name=selected_template_name).first()
#             if selected_template:
#                 name = st.text_input('Name', value=selected_template.name)
#                 purpose = st.text_area('Purpose', value=selected_template.purpose)
#                 template = st.text_area('Template', value=selected_template.template, height=None)  # Make the text area expand vertically
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button('Save', key="save_button"):
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
#             st.write(f"Name: {selected_template.name}")
#             st.write(f"Purpose: {selected_template.purpose}")
#             st.write(f"Template: {selected_template.template}")
#             prompt_template = ChatPromptTemplate.from_template(selected_template.template)                
#             input_variables = prompt_template.messages[0].prompt.input_variables
#             inputs = create_input_fields(input_variables)
#             # user_input = st.text_area("User Input")
#             if st.button("Submit"):
#                 # Process user input here
             
#                 # for var_name, var_value in inputs.items():
#                 #         st.write(f"{var_name}: {var_value}")                
#                 # st.write(f"User input: {user_input}")
#                 input_values = {}
#                 for var_name, var_value in inputs.items():
#                     input_values[var_name] = var_value

#                 # Update the call to format_messages with input values
#                 formatted_messages = prompt_template.format_messages(**input_values)
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

# Main function to run the Streamlit app
def main():
    st.sidebar.title('Select Action')

    action = st.sidebar.radio('Action', ['Display Editable Template', 'Load and Display Template'])

    if action == 'Display Editable Template':
        st.sidebar.title('Select Prompt Template')
        templates = session.query(PromptTemplate).all()
        template_names = ["New Template"]  # Make "New Template" the first option
        template_names.extend([template.name for template in templates])

        selected_template_name = st.sidebar.selectbox('Template', template_names)

        if selected_template_name == "New Template":
            selected_template = None
            st.empty()
            name = st.text_input('Name')
            purpose = st.text_area('Purpose')
            template = st.text_area('Template', height=None)  # Make the text area expand vertically
            if st.button('Save New Template'):
                if not name:
                    st.error('Please enter a name for the template!')
                else:
                    if name in template_names[1:]:
                        st.error('A template with this name already exists!')
                    else:
                        new_template = PromptTemplate(name=name, purpose=purpose, template=template)
                        session.add(new_template)
                        session.commit()
                        st.success('Template saved successfully!')
        else:
            selected_template = session.query(PromptTemplate).filter_by(name=selected_template_name).first()
            if selected_template:
                name = st.text_input('Name', value=selected_template.name)
                purpose = st.text_area('Purpose', value=selected_template.purpose)
                template = st.text_area('Template', value=selected_template.template, height=None)  # Make the text area expand vertically
                col1, col2 = st.columns(2)
                with col1:
                    if st.button('Save', key="save_button"):
                        if not name:
                            st.error('Please enter a name for the template!')
                        else:
                            if name != selected_template_name and name in template_names[1:]:
                                st.error('A template with this name already exists!')
                            else:
                                selected_template.name = name
                                selected_template.purpose = purpose
                                selected_template.template = template
                                session.commit()
                                st.success('Changes saved successfully!')
                with col2:
                    if st.button('Delete', key="delete_button"):
                        if selected_template:
                            session.delete(selected_template)
                            session.commit()
                            st.success('Template deleted successfully!')
    elif action == 'Load and Display Template':
        st.sidebar.title('Select Prompt Template')
        templates = session.query(PromptTemplate).all()
        template_names = [template.name for template in templates]

        selected_template_name = st.sidebar.selectbox('Template', template_names)

        selected_template = session.query(PromptTemplate).filter_by(name=selected_template_name).first()

        if selected_template:
            st.write(f"Name: {selected_template.name}")
            st.write(f"Purpose: {selected_template.purpose}")
            st.write(f"Template: {selected_template.template}")

             # Add a dropdown for selecting language model
            language_model = st.selectbox('Select Language Model', ['ChatGPT', 'Local Language Model'])
            if language_model == 'ChatGPT':
                pass
            elif language_model == 'Local Language Model':
                # Load your local language model here
                pass
            prompt_template = ChatPromptTemplate.from_template(selected_template.template)
            input_variables = prompt_template.messages[0].prompt.input_variables
            inputs = create_input_fields(input_variables)

            if st.button("Submit"):
                input_values = {}
                for var_name, var_value in inputs.items():
                    input_values[var_name] = var_value
                prompt = ChatPromptTemplate.from_template(selected_template.template)                
                formatted_messages = prompt.format_messages(**input_values)
                st.text_area(label='Prompt', value=formatted_messages)
               
if __name__ == '__main__':
    main()
