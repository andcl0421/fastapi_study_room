# 🏫 스터디룸 예약 시스템 (Study-Room-Reservation)

> **청년취업사관학교 도봉캠퍼스 AI 서비스 개발자 과정**
> 실무 관점의 데이터 설계와 검증 로직 구현을 위한 미니 프로젝트입니다.

---

## 1. 📂 프로젝트 구조 (Repository Structure)

* **study-room-reservation/** (최상위 루트)
    * `.gitignore` / `README.md` / `uv.lock`
    * **app/**
        * **models/** : [DB 설계도] SQLAlchemy 2.0 최신 문법(Mapped) 기반 테이블 정의
            * `__init__.py`: 모델 통합 임포트 및 DB 엔진 등록 관리
            * `user.py`: 사용자(Base 클래스 선언 포함)
            * `room.py`: 스터디룸 정보 및 시설 관리
            * `reservation.py`: 예약 핵심 데이터 및 상태 관리
            * `review.py`: 성능 최적화(역정규화)가 적용된 리뷰 관리
        * **schemas/** : [데이터 규격] Pydantic 모델 (Request/Response)
        * **services/** : [핵심 로직] 비즈니스 규칙 및 검증
        * **repositories/** : [창고 관리] DB CRUD 직접 수행
        * **routers/** : [안내 데스크] API 엔드포인트
        * `database.py`: PostgreSQL 연결 및 세션 관리
        * `main.py`: 애플리케이션 진입점

---

## 2. 🎯 기획 의도 (Why)

### 2.1 개발 배경
* 학생들이 스터디룸을 예약할 때 발생하는 **중복 예약 문제**와 **무분별한 독점**을 막기 위해 체계적인 예약 시스템이 필요했습니다.

### 2.2 해결하고자 하는 문제
* **중복 예약 방지**: 동일 시간대, 동일 강의실에 대한 중복 예약을 원천 차단합니다.
* **공정한 이용**: 하루 최대 이용 시간을 제한하여 특정 사용자의 독점을 방지합니다.
* **데이터 무결성**: 과거 날짜 예약 금지, 운영 시간 외 예약 금지 등 실무적인 검증 로직을 구현합니다.

---

## 3. 🏗️ 설계 및 구조 (Architecture)
![ERD 설계도](./app/docs/images/erd-1.0.png)

### 3.1 Layered Architecture
* **Router → Service → Repository → Model**로 이어지는 4계층 구조를 채택했습니다.
* **이유**: API 경로(Router)와 실제 비즈니스 규칙(Service)을 분리하여 코드의 유지보수성을 높이고, 테스트가 용이한 구조를 지향했습니다.

### 3.2 DB 모델링 전략 (ERD 핵심 포인트)
* **역정규화(Denormalization) 채택**: `Review` 테이블에 `user_id`와 `room_id`를 중복 포함시켰습니다.
    * **조회 성능**: 마이페이지 리뷰 목록 등 빈번한 조회 시 3-Way Join 비용을 제거했습니다.
    * **데이터 영속성**: 예약(`Reservation`) 데이터가 Soft/Hard Delete 되어도 리뷰의 주체 정보를 안정적으로 보존합니다.
* **실무 표준 명명 규칙**: 모든 필드에 **Snake Case**를 적용하고, PK 필드는 `테이블명_id` 형식을 사용하여 가독성을 확보했습니다.

---

## 4. 🛠️ 핵심 로직 및 기술 선택 이유 (Core Logic)

* **FastAPI**: 비동기 처리를 지원하며, Pydantic 기반의 강력한 타입 체킹과 자동 명세(Swagger) 생성을 위해 선택했습니다.
* **SQLAlchemy 2.0**: `Mapped`와 `mapped_column`을 사용한 최신 스타일의 타입 체킹 모델링으로 런타임 에러를 방지했습니다.
* **PostgreSQL**: 강력한 관계형 데이터베이스로, 실무 수준의 제약 조건(Constraints)과 인덱싱 최적화를 위해 채택했습니다.

---

## 5. 🚀 성장 포인트 (Retrospective)

### **[Troubleshooting: 정규화와 성능 사이의 의사결정]**
* **문제**: 리뷰 테이블 설계 시 `reservation_id`만 가질 경우(정규화), 조회 시마다 다중 Join이 발생하여 성능 저하 우려.
* **원인**: 실무에서는 데이터가 늘어날수록 Join 비용이 기하급수적으로 늘어날 수 있음.
* **해결**: 의도적으로 `user_id`, `room_id`를 중복 저장하는 **역정규화**를 수행. 대신 데이터 불일치를 방지하기 위해 서비스 계층에서 검증 로직을 강화하는 방향으로 설계함.
* **배운 점**: 데이터베이스 설계에 '절대적인 정답'은 없으며, 비즈니스 요구사항(성능 vs 무결성)에 따라 유연하게 트레이드오프(Trade-off)를 결정해야 함을 깨달음.

---

## 6. 📝 업데이트 기록 (Changelog)

* **v1.1**: ERD 설계 완료 및 `app/models/` 최신 SQLAlchemy 2.0 기반 구축 완료 (2026-02-19)
* **v1.0**: 프로젝트 초기 아키텍처 설계 및 환경 세팅 완료 (2026-02-19)