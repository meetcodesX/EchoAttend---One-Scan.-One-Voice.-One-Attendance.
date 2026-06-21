import streamlit as st

def main():
    st.header("This is my title")
    name = st.text_input("Enter a name : ")

    col1,col2 = st.columns(2,gap="medium")

    with col1:
        if st.button("click Here!",type="primary",key="bnt1",width="stretch"):
            print("Hello Mr.", name)
    
    with col2:
        if st.button("Click Here!",type="primary",key="bnt2",width="stretch"):
            print("bye ",name)

    st.markdown("""
                hi my name is meet currently pursing Btech
                <div>
                <h1> HII everyone</h1>
                </div>
""",unsafe_allow_html=True)

main()