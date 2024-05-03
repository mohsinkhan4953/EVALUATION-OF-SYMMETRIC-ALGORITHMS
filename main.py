import streamlit as st
from Crypto.Random import get_random_bytes
import dao, serpent, rc6
from database import engine,get_db
import models
models.Base.metadata.create_all(engine)
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from streamlit_option_menu import option_menu

description = """
## Performance Evaluation of Symmetric Algorithms

### RC6:
RC6 is a symmetric key block cipher derived from RC5. It was designed to meet the requirements of the Advanced Encryption Standard (AES) competition. RC6 has a variable block size, key size, and number of rounds.

### Serpent:
Serpent is a symmetric key block cipher that was a finalist in the AES competition. It is known for its security and efficiency in both software and hardware implementations. Serpent operates on blocks of data and has a fixed block size of 128 bits.

### MARS:
MARS (Matrix of Additive Rotation Substitutions) is a symmetric key block cipher developed by IBM. It supports a variable key length and block size, providing flexibility in its usage. MARS is designed to offer high security and performance.

### Twofish:
Twofish is a symmetric key block cipher designed to be highly secure and efficient. It supports block sizes of 128, 192, or 256 bits and key lengths of 128, 192, or 256 bits. Twofish operates on blocks of data using a series of substitution and permutation operations.

### AES (Advanced Encryption Standard):
AES is a symmetric key block cipher selected as the standard encryption algorithm by the U.S. National Institute of Standards and Technology (NIST). It supports key lengths of 128, 192, or 256 bits and has a fixed block size of 128 bits. AES has become widely adopted due to its security, efficiency, and simplicity.

---
"""
def test_performance():
    # Streamlit UI
    st.markdown(
        f"<h1 style='text-align: center;'>Performance Evaluation of Symmetric Algorithms</h1>",
        unsafe_allow_html=True,)
    st.markdown(description)
    st.subheader("Test Your File")

    uploaded_file = st.file_uploader("Upload a file")

    encryption_key = get_random_bytes(16)
    encryption_key_str = encryption_key.hex()

    algorithm_times = {}

    if uploaded_file is not None:
        st.success("File uploaded - Running tests...")

        file_contents = uploaded_file.read()

        # Calculate encryption and decryption times for each algorithm
        algorithm_times['AES'] = dao.aes_encrypt_decrypt(file_contents, encryption_key)
        st.info(f'AES: Encryption time: {algorithm_times["AES"][0]:.6f} seconds, Decryption time: {algorithm_times["AES"][1]:.6f} seconds')
        algorithm_times['Twofish'] = dao.twofish_encrypt_decrypt(file_contents, encryption_key_str)
        st.info(f'Twofish: Encryption time: {algorithm_times["Twofish"][0]:.6f} seconds, Decryption time: {algorithm_times["Twofish"][1]:.6f} seconds')
        algorithm_times['Serpent'] = serpent.serpent_encrypt_decrypt(file_contents, encryption_key_str)
        st.info(f'Serpent: Encryption time: {algorithm_times["Serpent"][0]:.6f} seconds, Decryption time: {algorithm_times["Serpent"][1]:.6f} seconds')
        algorithm_times['RC6'] = rc6.rc6_encrypt_decrypt(file_contents, encryption_key)
        st.info(f'RC6: Encryption time: {algorithm_times["RC6"][0]:.6f} seconds, Decryption time: {algorithm_times["RC6"][1]:.6f} seconds')
        algorithm_times['MARS'] = dao.mars_encrypt_decrypt(file_contents, encryption_key)
        st.info(f'MARS: Encryption time: {algorithm_times["MARS"][0]:.6f} seconds, Decryption time: {algorithm_times["MARS"][1]:.6f} seconds')
        print(algorithm_times)

        # Sort algorithms based on total time
        sorted_algorithm_times = sorted(algorithm_times.items(), key=lambda x: x[1])

        # Display results in a centered table
        table_data = [("Rank", "Algorithm", "Total Time (Encryption + Decryption)")]
        for idx, (algorithm, (encrypt_time, decrypt_time)) in enumerate(sorted_algorithm_times):
            table_data.append((idx+1, algorithm, f"{encrypt_time + decrypt_time:.6f} seconds"))

        st.table(table_data)
        # Store results in the database
        with SessionLocal() as db:
            new_record = models.Table(
                file_name=uploaded_file.name,
                aes_encrypt_time =algorithm_times['AES'][0],
                aes_decrypt_time=algorithm_times['AES'][1],
                serpent_encrypt_time=algorithm_times['Serpent'][0],
                serpent_decrypt_time=algorithm_times['Serpent'][1],
                rc6_encrypt_time=algorithm_times['RC6'][0],
                rc6_decrypt_time=algorithm_times['RC6'][1],
                mars_encrypt_time=algorithm_times['MARS'][0],
                mars_decrypt_time=algorithm_times['MARS'][1],
                twofish_encrypt_time=algorithm_times['Twofish'][0],
                twofish_decrypt_time=algorithm_times['Twofish'][1]
                
            )
            db.add(new_record)
            db.commit()

    else:
        st.error("Please upload a file")

def fetch_data():
    st.subheader("All test results")
    with SessionLocal() as db:
        # Fetch all records from the database
        records = db.query(models.Table).all()

        # Display the records in a table
        if records:
            table_data = []
            table_data.append(['id','file_name','aes_encrypt_time','aes_decrypt_time','serpent_encrypt_time','serpent_decrypt_time','rc6_encrypt_time','rc6_decrypt_time','mars_encrypt_time','mars_decrypt_time','twofish_encrypt_time','twofish_decrypt_time'])
            for record in records:
                # Extract data from each record
                row_data = [
                    record.id,
                    record.file_name,
                    record.aes_encrypt_time,
                    record.aes_decrypt_time,
                    record.serpent_encrypt_time,
                    record.serpent_decrypt_time,
                    record.rc6_encrypt_time,
                    record.rc6_decrypt_time,
                    record.mars_encrypt_time,
                    record.mars_decrypt_time,
                    record.twofish_encrypt_time,
                    record.twofish_decrypt_time
                ]
                table_data.append(row_data)
            
            # Display the data in a table
            st.table(table_data)
        else:
            st.write("No records found in the database.")




with st.sidebar:

    selected_option = option_menu("Options", ["Test Performance", "View past results", ], menu_icon="menu-up", icons=["cloud-upload", "folder"])


# Execute the selected option
if selected_option == "Test Performance":
    test_performance()
elif selected_option == "View past results":
    fetch_data()