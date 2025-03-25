# 모듈 임포트: CPU 정보, 시스템 자원 및 GPU 정보를 수집하기 위한 라이브러리
import cpuinfo      # CPU 관련 정보를 가져오기 위한 라이브러리
import psutil       # 시스템의 메모리, CPU, 프로세스 등 자원 정보 수집
import GPUtil       # GPU 정보를 수집하기 위한 라이브러리

# ----------------- CPU 정보 수집 -----------------
# cpuinfo를 사용하여 현재 CPU 정보를 가져옵니다.
cpu_info = cpuinfo.get_cpu_info()  # CPU의 상세 정보 딕셔너리로 반환
# psutil을 사용하여 물리적 코어와 논리적 코어의 수를 가져옵니다.
physical_cores = psutil.cpu_count(logical=False)  # 물리적 코어 수
logical_cores = psutil.cpu_count(logical=True)      # 논리적 코어 수

# CPU 정보 출력
print("[CPU Information]")  # 섹션 제목 출력
print(f"Processor: {cpu_info.get('brand_raw', 'N/A')}")  # CPU 브랜드 및 모델명 출력
print(f"Architecture: {cpu_info.get('arch', 'N/A')}")      # CPU 아키텍처 출력
print(f"Cores: {physical_cores} physical, {logical_cores} logical")  # 코어 수 출력
print(f"Base Frequency: {cpu_info.get('hz_actual_friendly', 'N/A')}")  # 기본 클럭 주파수 출력
print("")  # 줄바꿈

# ----------------- 메모리 정보 수집 -----------------
# psutil을 사용하여 시스템 메모리 정보를 가져옵니다.
mem_info = psutil.virtual_memory()  # 메모리 정보 객체 반환
# 메모리 총 용량을 기가바이트 단위로 변환하여 출력합니다.
print("[Memory Information]")  # 섹션 제목 출력
print(f"Total Memory: {mem_info.total / (1024 ** 3):.2f} GB")  # 총 메모리 용량 출력
print("")  # 줄바꿈

# ----------------- GPU 정보 수집 -----------------
# GPUtil을 사용하여 현재 시스템의 GPU 정보를 리스트 형태로 가져옵니다.
gpus = GPUtil.getGPUs()  # 시스템에 연결된 GPU 목록 반환
print("[GPU Information]")  # 섹션 제목 출력
if not gpus:
    # GPU가 감지되지 않을 경우 메시지 출력
    print("No GPU detected")
else:
    # 감지된 GPU 각각에 대해 정보를 출력
    for gpu in gpus:
        print(f"GPU Name: {gpu.name}")  # GPU 이름 출력
        print(f"Driver Version: {gpu.driver}")  # GPU 드라이버 버전 출력
        print(f"Memory Total: {gpu.memoryTotal} MB")  # GPU 전체 메모리 출력
        print(f"Memory Free: {gpu.memoryFree} MB")  # 사용 가능한 메모리 출력
        print(f"Memory Used: {gpu.memoryUsed} MB")  # 사용 중인 메모리 출력
        print(f"Temperature: {gpu.temperature} °C")  # 현재 온도 출력
        print("")  # 줄바꿈

# ----------------- 병목(Bottleneck) 분석 예시 -----------------
def bottleneck_analysis(cpu_score, gpu_score):
    """
    CPU와 GPU의 벤치마크 점수를 비교하여 병목 현상을 판단하는 함수
    - cpu_score: CPU의 성능 점수 (예: Cinebench 결과)
    - gpu_score: GPU의 성능 점수 (예: 3DMark 결과)
    반환:
    - 문자열로 병목 현상 가능성에 대한 설명 반환
    """
    # 단순 비율을 사용한 예시 로직: 특정 임계값 이상이면 병목으로 판단
    ratio = cpu_score / gpu_score  # CPU와 GPU 점수의 비율 계산
    if ratio > 1.2:
        return "GPU 병목 가능성 높음"  # CPU에 비해 GPU 성능이 부족할 가능성
    elif ratio < 0.8:
        return "CPU 병목 가능성 높음"  # GPU에 비해 CPU 성능이 부족할 가능성
    else:
        return "균형 잡힌 시스템"  # 대체로 균형 있는 시스템

# 예시: 임의의 점lysis(cpu_benchmark_score, gpu_benchmark_score))  # 분석 결과 출력
print("")  # 줄바꿈

# ----------------- 가격 크롤링 (간단 예시) -----------------
import requests      # HTTP 요청을 위해 사용
from bs4 import BeautifulSoup  # HTML 파싱을 위해 사용

def get_price_from_url(url):
    """
    지정된 URL로부터 가격 정보를 추출하는 함수 (간단한 예시)
    - url: 제품 가격 정보를 담고 있는 웹 페이지 URL
    반환:
    - 가격 정보 문자열 (실제 선택자는 해당 사이트에 맞게 수정 필요)
    """
    # 웹 페이지 요청
    response = requests.get(url)
    # 응답 받은 HTML을 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    # 예시: 'price' 클래스를 가진 첫 번째 요소에서 텍스트 추출 (실제 HTML 구조에 맞게 수정)
    price = soup.find("span", {"class": "price"}).text
    return price

# 실제 URL은 각 쇼핑몰의 제품 페이지 URL로 교체 필요
sample_product_url = "https://example.com/product"  # 예시 URL
# 아래 출력은 실제 동작하는 URL이 있을 때 의미 있음
# print("[Price Information]")
# print(f"Current Price: {get_price_from_url(sample_product_url)}")

# ----------------- 결론 -----------------
"""
Project SHA는 PC 조립과 업그레이드에 있어 사용자가 직관적으로 시스템 성능을 파악하고,
최적의 업그레이드 방향을 제시받을 수 있도록 하는 혁신적인 도구입니다.
- 실시간 하드웨어 정보 수집, 병목 분석, 벤치마크 시뮬레이션을 통해 사용자는 자신의 PC 상태를 명확히 이해할 수 있습니다.
- 업그레이드 추천과 가격 크롤링 기능을 통해 효율적인 투자 결정을 지원합니다.
- 추가 기능(커뮤니티, 로그 기록, API 제공 등)을 통해 확장성을 고려한 미래 지향적 플랫폼입니다.
"""

# 위 코드는 각 기능의 핵심 동작 원리를 간략하게나마 보여주며,
# 실제 제품 개발 시 이와 유사한 모듈이 통합되어 동작하게 됩니다.