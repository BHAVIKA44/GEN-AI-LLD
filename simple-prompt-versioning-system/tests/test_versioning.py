from simple_prompt_versioning_system.errors import PromptNotFoundError
from simple_prompt_versioning_system.service import PromptVersioningService
from simple_prompt_versioning_system.store import InMemoryPromptStore


def build_service() -> PromptVersioningService:
    return PromptVersioningService(InMemoryPromptStore())


def test_create_versions_and_list() -> None:
    service = build_service()
    v1 = service.create_version("support_reply", "Hello {{name}}")
    v2 = service.create_version("support_reply", "Hi {{name}}, how can I help?")

    versions = service.list_versions("support_reply")

    assert v1.version == 1
    assert v1.is_active is True
    assert v2.version == 2
    assert len(versions) == 2


def test_activate_version_switches_active_flag() -> None:
    service = build_service()
    service.create_version("qa_prompt", "v1")
    service.create_version("qa_prompt", "v2")

    active = service.activate_version("qa_prompt", 2)

    assert active.version == 2
    assert service.get_active("qa_prompt").version == 2


def test_get_missing_prompt_raises() -> None:
    service = build_service()

    try:
        service.list_versions("missing")
        assert False, "expected PromptNotFoundError"
    except PromptNotFoundError:
        pass


def test_get_specific_version() -> None:
    service = build_service()
    service.create_version("summarizer", "template v1")
    service.create_version("summarizer", "template v2")

    v2 = service.get_version("summarizer", 2)

    assert v2.template == "template v2"
