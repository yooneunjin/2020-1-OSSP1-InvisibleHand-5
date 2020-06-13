import create
import preprocess
import result
import analyze
import morphs
import emotion_word
import math
import pandas as pd
import noun_ex
import sys
from matplotlib import pyplot as plt

pd.set_option('mode.chained_assignment', None)

def main(fileName, name):


    book = open(f'../web/upload/{fileName}', "rt", encoding='UTF8', errors='ignore')
    # 전처리
    context = preprocess.remove_etc(book)

    # 변수 선언
    charOfPage = 700
    listOfEmotion = ['기쁨', '슬픔', '분노', '공포', '혐오', '놀람']
    numOfEmotion = len(listOfEmotion)
    numOfPage = math.ceil(len(context) / charOfPage)
    # numOfCharacter = int(input("등장인물 수 : "))
    # numOfCharacter = 1  # 테스트용 #########나중에 수정######################

    listOfCharacter = []
    listOfCharacter.append(name)
    numOfCharacter = len(listOfCharacter)

    # 사용자 사전 생성
    create.create_userdic(listOfCharacter)

    # 문장 테이블 생성
    df = create.create_sentence_dataframe(context, listOfEmotion)
    create.save_df(df, fileName)

    # 명사 추출
    # noun_ex.noun_extract(df)

    # emotion_word.emotion_lemmatization()

    # 문장 데이터프레임 생성
    df_sentence = create.create_sentence_dataframe(context, listOfEmotion)

    # 감정 사전 생성
    # emotion_dictionary_lists = emotion_word.create_emotion_dictionary()

    # 구축되어 있는 감정 사전 데이터 프레임 오픈
    df_emotion = emotion_word.open_emotion_dataframe()

    # 문장 분석
    df_sentence = analyze.analyze_sentence(df_sentence, listOfCharacter, df_emotion, charOfPage)
    create.save_df(df_sentence, fileName)

    df_sentence.to_html(justify='center')
    # 등장인물 별 페이지 감정 점수 합산하여 등장인물 데이터프레임 생성
    df_list_character = analyze.merge_character(df_sentence, listOfEmotion, listOfCharacter)

    # 그래프 설정
    result.config_graph()

    # 결과 1. 각 등장인물의 페이지별 감정 수준 그래프 생성 및 출력
    result.display_emotion_graph(df_list_character, listOfCharacter, numOfCharacter, listOfEmotion)

    # 결과 2. 모든 등장인물의 페이지별 감정 흐름 그래프 생성 및 출력
    # result.display_sentiment_graph(numOfCharacter, listOfCharacter, numOfPage, sentimentVector)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])