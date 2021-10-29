import sys
import os

from pathlib import Path
import pandas as pd

# pytest를 적절히 임포트하기 위해 필요합니다.
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from ml_editor.data_ingestion import parse_xml_to_csv

TEXT_LENGTH_FIELD = "text_len"

# 테스트를 위해 필요한 특성을 정의합니다.
REQUIRED_COLUMNS = [
    "Id",
    "AnswerCount",
    "PostTypeId",
    "AcceptedAnswerId",
    "Body",
    "body_text",
    "Title",
    "Score",
]

# 데이터 탐색에 기반하여 만들어진 간격
ACCEPTABLE_TEXT_LENGTH_MEANS = pd.Interval(left=20, right=2000)


def get_fixture_df():
    """
    파서를 사용해 데이터프레임을 반환합니다
    :return:
    """
    curr_path = Path(os.path.dirname(__file__))
    return parse_xml_to_csv(curr_path / Path("fixtures/MiniPosts.xml"))


def test_parser_returns_dataframe():
    """
    파서가 데이터프레임을 반환하는지 테스트합니다.
    """
    df = get_fixture_df()
    assert isinstance(df, pd.DataFrame)


def test_feature_columns_exist():
    """
    필수 열이 모두 들어 있는지 검사합니다.
    """
    df = get_fixture_df()
    for col in REQUIRED_COLUMNS:
        assert col in df.columns


def test_features_not_all_null():
    """
    누락된 값을 포함한 특성이 있는지 검사합니다.
    """
    df = get_fixture_df()
    for col in REQUIRED_COLUMNS:
        assert not df[col].isnull().all()


def test_text_mean():
    """
    텍스트 평균이 탐색 결과와 맞는지 검사합니다.
    """
    df = get_fixture_df()
    df["text_len"] = df["body_text"].str.len()
    text_col_mean = df["text_len"].mean()
    assert text_col_mean in ACCEPTABLE_TEXT_LENGTH_MEANS
