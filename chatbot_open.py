# 라이브러리 임포트
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import os


# OpenAI API 키 환경변수로 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPEN_AI_KEY"]

# 웹 페이지에 보여질 언어 목록
langs = ["Korean", "Spanish", "Chinese", "English"]
left_co, cent_co, last_co = st.columns(3)

# 사이드바에 라디오 버튼으로 언어 선택
with st.sidebar:
    language = st.radio("번역을 원하는 언어를 선택하세요", langs)
# 사용자 입력
st.markdown("### 언어 번역 서비스예요.")
prompt = st.text_input('번역을 원하는 텍스트를 입력해주세요.')

# 프롬프트 템플릿 정의
trans_template = PromptTemplate(
    input_variable = ['trans'],
    template = "Your task is to translate this text to "
        + language + ' TEXT : {trans}'
)

# 메모리 설정 (대화 이력 저장용)
memory = ConversationBufferMemory(input_key='trans', memory_key='chat_history')

# LLM 및 체인 구성
llm = ChatOpenAI(temperature = 0, model_name = 'gpt-4')
trans_chain = LLMChain(llm = llm, prompt = trans_template,
                       verbose = True, output_key = 'translate',
                       memory = memory)

# 번역 버튼 처리
if st.button('번역'):
    if prompt:
        response = trans_chain({'trans': prompt})
        st.info(response['translate'])