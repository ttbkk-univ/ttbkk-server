from src.utils.map import parse_address


def test_괄호를_없애줘야_한다():
    assert '서울특별시 서초구 잠원로 51' == parse_address('서울특별시 서초구 잠원로 51 (잠원동. 뉴코아아울렛 지하1층)')


def test_층수_다음_값들과_괄호를_없애줘야한다():
    assert '인천광역시 계양구 오조산공원로 14' == parse_address('인천광역시 계양구 오조산공원로 14, (계산동) 4층 일부호(홈플러스 계산점)')


def test_건물과_층이름을_없애야함():
    assert '경기 평택시 관광특구로 19 롯데시네마' == parse_address('경기 평택시 관광특구로 19 롯데시네마 건물 2층')


def test_몇동_몇호_인지는_없애야함():
    assert '경기 성남시 수정구 창업로 17' == parse_address('경기 성남시 수정구 창업로 17 A동 203-2호')


def test_몇호_인지만_있어도_날려줘():
    assert '경기 남양주시 다산중앙로 113 다산진건라페온빌' == parse_address('경기 남양주시 다산중앙로 113 다산진건라페온빌 113호')


def test_여러_호수에_있어도_날려줘():
    assert '인천 서구 청라루비로 76' == parse_address('인천 서구 청라루비로 76 224,225호')


def test_동만_있어도_날려줘():
    assert '인천 연수구 아트센터대로 87' == parse_address('인천 연수구 아트센터대로 87  401동')


def test_동_뒤에_문자가_있으면_날리면_안돼():
    assert '서울 성동구 한림말3길 21' == parse_address('서울 성동구 한림말3길 21')


def test_한글로_된_동_이름은_날리면_안됨():
    assert '울산 북구 산하동 산 61-4' == parse_address('울산 북구 산하동 산 61-4')
