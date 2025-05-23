# 마비노기 모바일 염색 도우미 🎨

마비노기 모바일의 염색 시스템에서 원하는 색상을 손쉽게 찾을 수 있도록 도와주는 Windows 전용 도구입니다.  
ROI(관심 영역) 내에서 지정한 색상을 실시간으로 감지하고 화면에 표시해줍니다.

---

## ⚠️ 유의사항

이 프로그램은 **비공식 사용자 제작 도구**입니다.  
사용 중 발생하는 문제나 피해에 대해서는 제작자가 책임지지 않으며, **모든 책임은 사용자 본인에게 있습니다.**

---

## 📦 설치 방법 (소스 코드 직접 빌드해서 사용)

1. `activate.bat` 실행  
   가상환경을 생성하고 활성화합니다.

2. `install.bat` 실행  
   필요한 Python 패키지를 자동으로 설치합니다.

3. `build.bat` 실행  
   실행 파일(`dye.exe`)을 생성합니다.

4. `dist` 폴더 내의 `dye.exe` 실행  
   설치 완료! 프로그램을 바로 사용할 수 있습니다.

---

### 🔽 다운로드 (빌드된거 사용)
[dye.exe v0.1](https://github.com/LolotiEE/mmdye/releases/tag/v0.1)

---

## ✅ 주요 기능

- 관심 영역(ROI) 지정 및 크기 조절
- 두 가지 색상 동시 감지
- 오차 범위 설정
- 실시간 화면 표시 (색상 위치 점멸)

---

## 💡 사용 환경

- Windows 10 이상
- Python 3.10 (가상환경 내 자동 구성)

---

## 📝 라이선스

본 프로젝트는 별도의 라이선스를 적용하지 않으며, 모든 저작권은 개발자에게 있습니다.  
무단 복제 및 재배포는 금합니다.
