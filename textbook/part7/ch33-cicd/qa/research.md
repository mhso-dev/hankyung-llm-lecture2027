# Ch33 공식 문서 조사

확인일: 2026-09-11

- GitHub Actions 공식 문서는 workflow가 저장소 이벤트로 시작되고 job과 step으로 구성되며, Python 프로젝트에서 `setup-python`, 테스트, Ruff, 아티팩트 보관을 사용할 수 있다고 설명합니다. 본문은 PR에서 자동 검사를 실행하는 범위만 반영했습니다.
- Docker 공식 문서는 `docker image push`가 이미지를 레지스트리에 공유하며 push 결과에 digest가 표시되는 예를 제공합니다. 본 실습은 네트워크 push 없이 바이트의 SHA-256 변화만 확인합니다.
- Kubernetes 공식 문서는 Deployment의 rollout 상태 확인과 `kubectl rollout undo`를 통한 이전 리비전 복구를 설명합니다. 본 실습은 클러스터 없이 JSON 이력으로 같은 상태 전이를 축소 재현합니다.
- Prometheus 3.5 공식 문서는 표현식과 조건으로 경보 규칙을 정의하고 외부 서비스로 알림을 보낼 수 있다고 설명합니다. 본 실습은 외부 전송 없이 고정 메트릭 판정만 수행합니다.

기준 URL은 각 절 참고 자료에 직접 연결했습니다. GitHub의 현재 예시에 표시된 Actions 주요 버전은 향후 바뀔 수 있으므로 실제 수업 직전에 다시 확인해야 합니다.
