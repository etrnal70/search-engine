from src.indexing.inverted_index import Indexer, WordInfo, UserQuery, CAPITAL_PATTERN, getDocID, getPosition
from src.database.database import Database
from re import match
from dotenv import load_dotenv
from os import getenv
from typing import Dict, List, Union, Tuple

# TODO Remaining tests
# - Empty hitlists
# - Commond words hitlists
# - Scoring

# Indexer test case
# Using pytest

load_dotenv()
db = Database()

repository: List[Dict[str, Union[int, str]]] = [{
    "page_id":
    1,
    "paragraph":
    "Pease porridge hot, pease porridge cold,"
}, {
    "page_id":
    2,
    "paragraph":
    "Pease porridge in the pot,"
}, {
    "page_id": 3,
    "paragraph": "Nine days old."
}, {
    "page_id":
    4,
    "paragraph":
    "Some like it hot, some like it cold,"
}, {
    "page_id":
    5,
    "paragraph":
    "Some like it in the pot,"
}, {
    "page_id": 6,
    "paragraph": "Nine days old."
}]


class TestCapitalCheck:

    def test_middle(self):
        assert bool(match(CAPITAL_PATTERN, "CoWoS")) == True

    def test_allUpper(self):
        assert bool(match(CAPITAL_PATTERN, "DARPA")) == True

    def test_firstOnly(self):
        assert bool(match(CAPITAL_PATTERN, "Asahi")) == False

    def test_lastOnly(self):
        assert bool(match(CAPITAL_PATTERN, "asahI")) == False


class TestInvertedIndex:

    def test_hitlists(self):

        idx = Indexer(db, str(getenv("INDEXER_STATUS")))
        idx.generateIndex(repository)
        porridgeList = idx.pairs["porridge"]

        # Evaluate total unique words
        assert len(idx.pairs) == 13

        # Evaluate porridge hit counts
        assert len(porridgeList) == 3

        noPorridgeDoc = [3, 4, 5, 6]
        porridgeDoc = [1, 2]

        # Evaluate hit data
        for data in porridgeList:
            docID = data >> 13
            assert docID not in noPorridgeDoc
            assert docID in porridgeDoc

    def test_parse_input(self):
        idx = Indexer(db, str(getenv("INDEXER_STATUS")))
        idx.generateIndex(repository)

        input: str = "porridge hot"
        expectedPairs: Dict[str, WordInfo] = {
            "porridge": (1, False, False),
            "hot": (2, False, False),
        }

        parseResults = idx.parseInput(input)
        assert parseResults == expectedPairs

    def test_query(self):
        query = UserQuery()
        idx = Indexer(db, str(getenv("INDEXER_STATUS")))
        idx.generateIndex(repository)

        input: str = "porridge hot"
        expectedPairs: Dict[str, Tuple[WordInfo, List[int]]] = {  #type: ignore
            "porridge": ((1, False, False), idx.pairs["porridge"]),
            "hot": ((2, False, False), idx.pairs["hot"])
        }

        parseResults = idx.parseInput(input)
        idx.getInputPairs(query, parseResults)

        assert query.pairs == expectedPairs

    def test_query_merge(self):
        query = UserQuery()
        idx = Indexer(db, str(getenv("INDEXER_STATUS")))
        idx.generateIndex(repository)

        input: str = "porridge hot"

        parseResults = idx.parseInput(input)
        idx.getInputPairs(query, parseResults)
        query.processQuery()

        assert len(query.mergedHitlists) > 0

        posResult: List[int] = []  #type: ignore
        for item in query.mergedHitlists:
            assert getDocID(item) in [1, 2]
            posResult.append(getPosition(item))

        assert posResult == [2, 3, 5, 2]

    # def test_merge_empty(self):
    #     idx = Indexer(db, str(getenv("INDEXER_STATUS")))
    #     idx.generateIndex(repository)
    #     idx.convert()

    # def test_merge_usejaccard(self):
    #     idx = Indexer(db, str(getenv("INDEXER_STATUS")))
    #     idx.generateIndex(repository)
    #     idx.convert()

    # def test_merge2(self):
    #     idx = Indexer(db, str(getenv("INDEXER_STATUS")))
    #     idx.generateIndex(repository)
    #     idx.convert()
    #
    #     wordInfos: List[Tuple[WordInfo, Optional[HitLists]]] = [  #type: ignore
    #         ((1, False, False), idx.pairs["hot"]),
    #         ((2, False, False), idx.pairs["like"])
    #     ]
    #
    #     result = idx.mergeHitlists(wordInfos)
    #
    #     assert wordInfos[0] in result[0]
    #     assert wordInfos[1] in result[0]
