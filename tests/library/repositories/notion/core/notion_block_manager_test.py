import os, sys

sys.path.insert(0, os.path.abspath("."))

from main.library.di_container import Container
from main.library.repositories.notion.core.notion_block_manager import (
    NotionBlockManager,
)

container: Container = Container()
notion_block_manager: NotionBlockManager = container.notion_block_manager()


def test_should_read_page_blocks_by_page_id(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"list","results":[{"object":"block","id":"4dd595a3-bf18-4e14-938e-95a44ac77d72","parent":{"type":"page_id","page_id":"48a4c8b5-8c75-43ee-8863-505c38ffa20e"},"created_time":"2024-05-24T01:47:00.000Z","last_edited_time":"2024-05-24T01:47:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"has_children":false,"archived":false,"in_trash":false,"type":"image","image":{"caption":[],"type":"external","external":{"url":"https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb"}}}],"next_cursor":null,"has_more":false,"type":"block","block":{},"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"39cfbb1e-4f4d-461c-8015-fbf8701642c3"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)

    # Arrange
    page_id: str = "c5353a8c-a89c-4dd0-96c5-e3e2d19a0387"

    # Act
    response_blocks: dict = notion_block_manager.read_page_blocks_by_page_id(page_id)

    # Assert
    assert response_blocks is not None, "Page blocks not found"
    assert "has_more" in response_blocks, "Page blocks has_more is empty"
    assert response_blocks["has_more"] is not None, "Page blocks has_more is empty"
    assert "next_cursor" in response_blocks, "Page blocks next_cursor is empty"
    assert "blocks" in response_blocks, "Page blocks blocks is empty"
    assert response_blocks["blocks"] is not None, "Page blocks blocks is empty"
    assert len(response_blocks["blocks"]) > 0, "Page blocks blocks is empty"
