from sqlalchemy import Column, Integer, String, Float
from database import Base 
class Table(Base):
    __tablename__='previous_records'
    id=Column(Integer, primary_key=True, index=True)
    file_name=Column(String)
    aes_encrypt_time =Column(Float)
    aes_decrypt_time=Column(Float)
    serpent_encrypt_time=Column(Float)
    serpent_decrypt_time=Column(Float)
    rc6_encrypt_time=Column(Float)
    rc6_decrypt_time=Column(Float)
    mars_encrypt_time=Column(Float)
    mars_decrypt_time=Column(Float)
    twofish_encrypt_time=Column(Float)
    twofish_decrypt_time=Column(Float)