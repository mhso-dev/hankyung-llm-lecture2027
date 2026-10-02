# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**chatStreamV1ChatStreamPost**](DefaultApi.md#chatstreamv1chatstreampost) | **POST** /v1/chat/stream | Chat Stream |
| [**chatV1ChatPost**](DefaultApi.md#chatv1chatpost) | **POST** /v1/chat | Chat |
| [**healthHealthGet**](DefaultApi.md#healthhealthget) | **GET** /health | Health |
| [**liveChatStreamV1ChatLiveStreamPost**](DefaultApi.md#livechatstreamv1chatlivestreampost) | **POST** /v1/chat/live/stream | Live Chat Stream |
| [**liveChatV1ChatLivePost**](DefaultApi.md#livechatv1chatlivepost) | **POST** /v1/chat/live | Live Chat |



## chatStreamV1ChatStreamPost

> chatStreamV1ChatStreamPost(chatRequest, authorization, lastEventID)

Chat Stream

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { ChatStreamV1ChatStreamPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // ChatRequest
    chatRequest: ...,
    // string (optional)
    authorization: authorization_example,
    // string (optional)
    lastEventID: lastEventID_example,
  } satisfies ChatStreamV1ChatStreamPostRequest;

  try {
    const data = await api.chatStreamV1ChatStreamPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **chatRequest** | [ChatRequest](ChatRequest.md) |  | |
| **authorization** | `string` |  | [Optional] [Defaults to `undefined`] |
| **lastEventID** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `text/event-stream`, `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## chatV1ChatPost

> ChatResponse chatV1ChatPost(chatRequest, authorization)

Chat

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { ChatV1ChatPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // ChatRequest
    chatRequest: ...,
    // string (optional)
    authorization: authorization_example,
  } satisfies ChatV1ChatPostRequest;

  try {
    const data = await api.chatV1ChatPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **chatRequest** | [ChatRequest](ChatRequest.md) |  | |
| **authorization** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

[**ChatResponse**](ChatResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## healthHealthGet

> HealthResponse healthHealthGet()

Health

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { HealthHealthGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.healthHealthGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**HealthResponse**](HealthResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## liveChatStreamV1ChatLiveStreamPost

> liveChatStreamV1ChatLiveStreamPost(chatRequest, authorization)

Live Chat Stream

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { LiveChatStreamV1ChatLiveStreamPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // ChatRequest
    chatRequest: ...,
    // string (optional)
    authorization: authorization_example,
  } satisfies LiveChatStreamV1ChatLiveStreamPostRequest;

  try {
    const data = await api.liveChatStreamV1ChatLiveStreamPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **chatRequest** | [ChatRequest](ChatRequest.md) |  | |
| **authorization** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `text/event-stream`, `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## liveChatV1ChatLivePost

> ChatResponse liveChatV1ChatLivePost(chatRequest, authorization)

Live Chat

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { LiveChatV1ChatLivePostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // ChatRequest
    chatRequest: ...,
    // string (optional)
    authorization: authorization_example,
  } satisfies LiveChatV1ChatLivePostRequest;

  try {
    const data = await api.liveChatV1ChatLivePost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **chatRequest** | [ChatRequest](ChatRequest.md) |  | |
| **authorization** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

[**ChatResponse**](ChatResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

