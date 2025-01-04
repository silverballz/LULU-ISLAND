import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up Streamlit app
st.title("Udemy Course Enrollment Analysis")
st.sidebar.header("Udemy Course Data Exploration")

# Upload dataset
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Dataset Overview", df.head())
    
    # Drop unnecessary columns
    columns_to_drop = ["id", "url", "is_paid", "headline", "objectives", "curriculum"]
    df = df.drop(columns=columns_to_drop, errors="ignore")

    # Filtered dataset
    df = df.head(98104)

    # Analysis Options
    analysis = st.sidebar.selectbox(
        "Select Analysis:",
        [
            "Overview",
            "Maximum and Minimum Enrollments",
            "Subject-wise Analysis",
            "Level-wise Analysis",
            "Maximum and Minimum Reviews",
            "Correlation Analysis",
        ],
    )

    # Maximum and Minimum Enrollments
    if analysis == "Maximum and Minimum Enrollments":
        st.subheader("1. Maximum and Minimum Enrollments")
        max_enrollments = df['num_subscribers'].max()
        min_enrollments = df['num_subscribers'].min()

        st.write("#### Course with Maximum Enrollments")
        st.write(df[df['num_subscribers'] == max_enrollments])

        st.write("#### Course with Minimum Enrollments")
        st.write(df[df['num_subscribers'] == min_enrollments])

    # Subject-wise Analysis
    elif analysis == "Subject-wise Analysis":
        st.subheader("2. Subject-wise Analysis")
        df_subjectwise = df.groupby(['category'], as_index=False)['num_subscribers'].sum()
        fig, ax = plt.subplots()
        sns.barplot(data=df_subjectwise, x="category", y="num_subscribers", ax=ax)
        plt.xticks(rotation=90)
        plt.title("Number of Subscribers by Category")
        st.pyplot(fig)

    # Level-wise Analysis
    elif analysis == "Level-wise Analysis":
        st.subheader("3. Level-wise Analysis")
        df_levelwise = df.groupby(['instructional_level'], as_index=False)['num_subscribers'].sum()
        fig, ax = plt.subplots()
        sns.barplot(data=df_levelwise, x="instructional_level", y="num_subscribers", ax=ax)
        plt.title("Number of Subscribers by Instructional Level")
        st.pyplot(fig)

    # Maximum and Minimum Reviews
    elif analysis == "Maximum and Minimum Reviews":
        st.subheader("4. Maximum and Minimum Reviews")
        max_reviews = df['num_reviews'].max()
        min_reviews = df['num_reviews'].min()

        st.write("#### Course with Maximum Reviews")
        st.write(df[df['num_reviews'] == max_reviews])

        st.write("#### Course with Minimum Reviews")
        st.write(df[df['num_reviews'] == min_reviews])

    # Correlation Analysis
    elif analysis == "Correlation Analysis":
        st.subheader("5. Correlation Analysis")
        df_2000 = df.sort_values("num_subscribers", ascending=False).head(2000)

        st.write("#### Correlation Between Reviews and Subscribers")
        correlation_reviews = df_2000["num_reviews"].corr(df_2000["num_subscribers"])
        st.write(f"Correlation: {correlation_reviews:.2f}")

        fig, ax = plt.subplots()
        sns.scatterplot(data=df_2000, x="num_reviews", y="num_subscribers", ax=ax)
        plt.title("Reviews vs. Subscribers")
        st.pyplot(fig)

        st.write("#### Correlation Between Rating and Subscribers")
        correlation_ratings = df_2000["rating"].corr(df_2000["num_subscribers"])
        st.write(f"Correlation: {correlation_ratings:.2f}")

    # Conclusion
    if st.sidebar.checkbox("Show Conclusion"):
        st.subheader("Conclusion")
        st.write(
            """
            - The "Development" category has the highest demand.
            - Courses oriented around Python Development are most popular.
            - There is a positive correlation between the number of reviews and subscribers.
            """
        )
else:
    st.write("Please upload a CSV file to proceed.")
