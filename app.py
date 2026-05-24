import streamlit as st
import mysql.connector
import pandas as pd
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="🎓 Assignment Submission System",
    layout="wide"
)

# =====================================================
# BEAUTIFUL DARK UI
# =====================================================

st.markdown("""
<style>

.stApp{
    background-color:#0B1120;
    color:white;
}

h1,h2,h3,h4{
    color:#38BDF8;
}

.card{
    background:#111827;
    padding:25px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 0px 10px rgba(255,255,255,0.1);
}

.stButton>button{
    background:#2563EB;
    color:white;
    border-radius:10px;
    height:45px;
    width:100%;
    border:none;
    font-size:16px;
}

.stButton>button:hover{
    background:#1D4ED8;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2a9926",
    database="semester_submission_system"
)

cursor = conn.cursor(buffered=True)

# =====================================================
# CREATE UPLOADS FOLDER
# =====================================================

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# =====================================================
# SESSION
# =====================================================

if "auth" not in st.session_state:
    st.session_state.auth = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.auth:

    st.title("🎓 Assignment Submission System")

    

    st.write("")

    col1, col2, col3 = st.columns(3)

    # ================= STUDENT =================

    with col1:

        st.markdown("""
        <div class='card'>
        <h2>👨‍🎓 Student</h2>
        <p>Submit Assignments 📤</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Student Login"):
            st.session_state.role = "student"

    # ================= TEACHER =================

    with col2:

        st.markdown("""
        <div class='card'>
        <h2>👨‍🏫 Teacher</h2>
        <p>Check & Grade 🏆</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Teacher Login"):
            st.session_state.role = "teacher"

    # ================= ADMIN =================

    with col3:

        st.markdown("""
        <div class='card'>
        <h2>🛠 Admin</h2>
        <p>Manage System ⚙️</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Admin Login"):
            st.session_state.role = "admin"

    # =====================================================
    # LOGIN INPUTS AFTER CLICK
    # =====================================================

    if st.session_state.role != "":

        st.write("---")

        st.subheader(f"🔐 {st.session_state.role.upper()} LOGIN")

        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("Login 🚀"):

            if username and password:

                st.session_state.auth = True
                st.session_state.username = username

                st.rerun()

            else:
                st.error("Enter Username & Password")

# =====================================================
# DASHBOARD
# =====================================================

else:

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.title("📌 MENU")

    st.sidebar.success(
        f"👤 {st.session_state.username}"
    )

    st.sidebar.info(
        f"🎭 Role: {st.session_state.role}"
    )

    # ================= LOGOUT =================

    if st.sidebar.button("🚪 Logout"):

        st.session_state.auth = False
        st.session_state.role = ""
        st.session_state.username = ""

        st.rerun()

    # ================= MENU =================

    menu = st.sidebar.selectbox(
        "Select Option",
        [
            "Home",
            "Add Student",
            "Add Teacher",
            "Add Course",
            "Add Assignment",
            "Submit Assignment",
            "View Courses",
            "View Assignments",
            "View Submissions",
            "Grade System",
            "View Results"
        ]
    )

    # =====================================================
    # HOME
    # =====================================================

    if menu == "Home":

        st.title("🎓 Assignment Submission System")

        st.markdown("## 🌸 Welcome To Our System ✨")
        st.markdown("### 💡 Learn • Submit • Improve • Succeed 🚀")

    # =====================================================
    # ADD STUDENT
    # =====================================================

    elif menu == "Add Student":

        st.subheader("👨‍🎓 Add Student")

        student_name = st.text_input("Student Name")
        roll_no = st.text_input("Roll Number")
        password = st.text_input("Password", type="password")

        if st.button("Save Student"):

            if student_name and roll_no and password:

                cursor.execute("""
                    INSERT INTO students(name, roll_no, password)
                    VALUES(%s,%s,%s)
                """, (
                    student_name,
                    roll_no,
                    password
                ))

                conn.commit()

                st.success("Student Added Successfully ✔️")

            else:
                st.error("Fill all fields")

        cursor.execute("""
            SELECT student_id, name, roll_no
            FROM students
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Student ID",
                    "Name",
                    "Roll No"
                ]
            )

            st.dataframe(df)

    # =====================================================
    # ADD TEACHER
    # =====================================================

    elif menu == "Add Teacher":

        st.subheader("👨‍🏫 Add Teacher")

        teacher_name = st.text_input("Teacher Name")
        email = st.text_input("Teacher Email")
        subject = st.text_input("Subject")
        password = st.text_input("Password", type="password")

        if st.button("Save Teacher"):

            if teacher_name and email and subject and password:

                cursor.execute("""
                    INSERT INTO teachers
                    (name, email, subject, password)
                    VALUES(%s,%s,%s,%s)
                """, (
                    teacher_name,
                    email,
                    subject,
                    password
                ))

                conn.commit()

                st.success("Teacher Added Successfully ✔️")

            else:
                st.error("Fill all fields")

        cursor.execute("""
            SELECT teacher_id,
                   name,
                   email,
                   subject
            FROM teachers
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Teacher ID",
                    "Teacher Name",
                    "Email",
                    "Subject"
                ]
            )

            st.dataframe(df)

    # =====================================================
    # ADD COURSE
    # =====================================================

    elif menu == "Add Course":

        st.subheader("📚 Add Course")

        course_id = st.text_input("Course ID")
        course_name = st.text_input("Course Name")

        if st.button("Save Course"):

            if course_id and course_name:

                cursor.execute("""
                    INSERT INTO courses(course_id, course_name)
                    VALUES(%s,%s)
                """, (
                    course_id,
                    course_name
                ))

                conn.commit()

                st.success("Course Added Successfully ✔️")

            else:
                st.error("Fill all fields")

        cursor.execute("""
            SELECT course_id,
                   course_name
            FROM courses
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Course ID",
                    "Course Name"
                ]
            )

            st.dataframe(df)

    # =====================================================
    # ADD ASSIGNMENT
    # =====================================================

    elif menu == "Add Assignment":

        st.subheader("📝 Create Assignment")

        title = st.text_input("Assignment Title")
        description = st.text_area("Description")

        cursor.execute("""
            SELECT course_id, course_name
            FROM courses
        """)

        courses = cursor.fetchall()

        course_map = {
            f"{c[0]} - {c[1]}": c[0]
            for c in courses
        }

        selected_course = st.selectbox(
            "Select Course",
            list(course_map.keys())
        )

        if st.button("Create Assignment"):

            cursor.execute("""
                INSERT INTO assignments
                (title, description, course_id)
                VALUES(%s,%s,%s)
            """, (
                title,
                description,
                course_map[selected_course]
            ))

            conn.commit()

            st.success("Assignment Created ✔️")

        cursor.execute("""
            SELECT a.assignment_id,
                   a.title,
                   c.course_name
            FROM assignments a
            JOIN courses c
            ON a.course_id = c.course_id
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Assignment ID",
                    "Title",
                    "Course"
                ]
            )

            st.dataframe(df)

    # =====================================================
    # SUBMIT ASSIGNMENT
    # =====================================================

    elif menu == "Submit Assignment":

        st.subheader("📤 Submit Assignment")

        student_id = st.number_input(
            "Student ID",
            min_value=1
        )

        cursor.execute("""
            SELECT course_id,
                   course_name
            FROM courses
        """)

        courses = cursor.fetchall()

        course_map = {
            f"{c[0]} - {c[1]}": c[0]
            for c in courses
        }

        selected_course = st.selectbox(
            "Select Course",
            list(course_map.keys())
        )

        cursor.execute("""
            SELECT assignment_id,
                   title
            FROM assignments
            WHERE course_id = %s
        """, (course_map[selected_course],))

        assignments = cursor.fetchall()

        assignment_map = {
            a[1]: a[0]
            for a in assignments
        }

        selected_assignment = st.selectbox(
            "Select Assignment",
            list(assignment_map.keys())
        )

        uploaded_file = st.file_uploader(
            "Upload File"
        )

        if st.button("Submit Assignment"):

            file_path = ""

            if uploaded_file:

                file_path = os.path.join(
                    "uploads",
                    uploaded_file.name
                )

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())

            cursor.execute("""
                INSERT INTO submissions
                (assignment_id, student_id, file_path)
                VALUES(%s,%s,%s)
            """, (
                assignment_map[selected_assignment],
                student_id,
                file_path
            ))

            conn.commit()

            st.success("Assignment Submitted ✔️")

    # =====================================================
    # VIEW COURSES
    # =====================================================

    elif menu == "View Courses":

        st.subheader("📚 All Courses")

        cursor.execute("""
            SELECT course_id,
                   course_name
            FROM courses
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Course ID",
                    "Course Name"
                ]
            )

            st.dataframe(df)

        else:
            st.warning("No Courses Found")

    # =====================================================
    # VIEW ASSIGNMENTS
    # =====================================================

    elif menu == "View Assignments":

        st.subheader("📝 All Assignments")

        cursor.execute("""
            SELECT a.assignment_id,
                   a.title,
                   c.course_name
            FROM assignments a
            JOIN courses c
            ON a.course_id = c.course_id
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Assignment ID",
                    "Title",
                    "Course"
                ]
            )

            st.dataframe(df)

        else:
            st.warning("No Assignments Found")

    # =====================================================
    # VIEW SUBMISSIONS
    # =====================================================

    elif menu == "View Submissions":

        st.subheader("📂 All Submissions")

        cursor.execute("""
            SELECT s.name,
                   a.title,
                   c.course_name
            FROM submissions sub
            JOIN students s
            ON sub.student_id = s.student_id
            JOIN assignments a
            ON sub.assignment_id = a.assignment_id
            JOIN courses c
            ON a.course_id = c.course_id
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Student",
                    "Assignment",
                    "Course"
                ]
            )

            st.dataframe(df)

        else:
            st.warning("No Submissions Found")

    # =====================================================
    # GRADE SYSTEM
    # =====================================================

    elif menu == "Grade System":

        st.subheader("🏆 Grade System")

        cursor.execute("""
            SELECT sub.submission_id,
                   s.name,
                   a.title
            FROM submissions sub
            JOIN students s
            ON sub.student_id = s.student_id
            JOIN assignments a
            ON sub.assignment_id = a.assignment_id
        """)

        submissions = cursor.fetchall()

        submission_map = {
            f"{s[1]} - {s[2]}": s[0]
            for s in submissions
        }

        selected_submission = st.selectbox(
            "Select Submission",
            list(submission_map.keys())
        )

        marks = st.number_input(
            "Marks",
            min_value=0,
            max_value=100
        )

        feedback = st.text_area("Feedback")

        if st.button("Save Grade"):

            cursor.execute("""
                INSERT INTO grades
                (submission_id, marks, feedback)
                VALUES(%s,%s,%s)
            """, (
                submission_map[selected_submission],
                marks,
                feedback
            ))

            conn.commit()

            st.success("Grade Saved ✔️")

        cursor.execute("""
            SELECT s.name,
                   a.title,
                   g.marks,
                   g.feedback
            FROM grades g
            JOIN submissions sub
            ON g.submission_id = sub.submission_id
            JOIN students s
            ON sub.student_id = s.student_id
            JOIN assignments a
            ON sub.assignment_id = a.assignment_id
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Student",
                    "Assignment",
                    "Marks",
                    "Feedback"
                ]
            )

            st.dataframe(df)

    # =====================================================
    # VIEW RESULTS
    # =====================================================

    elif menu == "View Results":

        st.subheader("📊 Student Results")

        cursor.execute("""
            SELECT s.name,
                   c.course_name,
                   a.title,
                   g.marks,
                   g.feedback
            FROM grades g
            JOIN submissions sub
            ON g.submission_id = sub.submission_id
            JOIN students s
            ON sub.student_id = s.student_id
            JOIN assignments a
            ON sub.assignment_id = a.assignment_id
            JOIN courses c
            ON a.course_id = c.course_id
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Student",
                    "Course",
                    "Assignment",
                    "Marks",
                    "Feedback"
                ]
            )

            st.dataframe(df)

        else:
            st.warning("No Results Found")