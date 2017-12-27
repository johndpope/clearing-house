# Clearing House API

* **Event**
    - [Create new event](#create-new-event)
    - [Get event](#get-event)
    - [Get events by tag](#get-events-by-tag)
    - [Edit event](#edit-event)
* **Tag**
    - [Create new tag](#create-new-tag)
    - [Edit tag](#edit-tag)
    - [Delete tag](#delete-tag)
    - [Get tags](#get-tags)


Every response is either JSON or an empty one with status code 200. A generic JSON response seems like
```json
{
  "status": "ok",
  <optional_fields>
}
```

Responses for erroneous requests seem like
```json
{
  "status": "error",
  "code": "<error code>",
  <optional_fields>
}
```

In particular, form validation errors cause the following response:
```json
{
  "status": "error",
  "code": "validation_error",
  "errors": {"<field_name>": "<error_description>"}
}
```

## <a name="create-new-event"/> Create new event
Field content can have arbitrary value.

```POST /api/v1/event/```

#### Headers
```Content-Type: "application/json"```

#### Content
```json
{
  "content": {
    "translates": {
      "ru": {
        "description": "\u0422\u0435\u0441\u0442\u043e\u0432\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435",
        "title": "\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a"
      },
      "en": {
        "description": "Test description",
        "title": "Title"
      }
    },
    "name": "test_event_2",
    "background": "goatsy.jpg"
  },
  "outcomes": [
    {
      "content": {
        "translates": {
          "ru": {
            "label": "\u0414\u0430"
          },
          "en": {
            "label": "Yes"
          }
        },
        "background": "yes.jpg"
      }
    },
    {
      "content": {
        "translates": {
          "ru": {
            "label": "\u041d\u0435\u0442"
          },
          "en": {
            "label": "No"
          }
        },
        "background": "no.jpg"
      }
    }
  ],
  "tags": ["politics", "science"]
}
```

#### Errors
```validation_error```

## <a name="get-event"/> Get event
```GET /api/v1/event/<int:event_id>/?lang=<string:lang>&raw=<int:raw>```

#### Parameters
```lang```  - language of translations

```raw```  - if 1 then get data without translation substitutions

#### Response
```json
{
  "event": {
    "content": {
      "name": "test_event_1"
    },
    "create_timestamp": 1514907875,
    "event_timestamp": null,
    "id": 1,
    "outcomes": [
      {
        "balance": 0,
        "bitcoin_address": "mtpCDrUCe6BsARmx9khWRAKfcqaBHoSQPC",
        "content": {
          "background": "3.jpg",
          "label": "yes"
        }
      },
      {
        "balance": 0,
        "bitcoin_address": "mwSs6HWFr1rGCTU7b5Amsz4M6PnB2AWezq",
        "content": {
          "background": "2.jpg",
          "label": "no"
        }
      }
    ],
    "state": "preparing",
    "tags": [
      {
        "name": "science"
      },
      {
        "name": "politics"
      }
    ]
  },
  "status": "ok"
}
```

#### Errors
```unknown_language_error```, ```nonexistent_entity_error```

## <a name="get-events-by-tag"/> Get events by tag
```GET /api/v1/tag/<string:tag_name>/?lang=<str:lang>&state=<str:state>```

#### Parameters
```lang``` - language of translations

```state``` - filter events by one of the following state: preparing, ongoing, holding, clearing, ended, deleted

#### Response
```json
{
  "events": [
    {
      "content": {
        "name": "test_event_1"
      },
      "create_timestamp": 1514978836,
      "event_timestamp": null,
      "id": 1,
      "outcomes": [
        {
          "bitcoin_address": "mxeGGMyFP2WP6q97z5VfF4QVcYczeMHBEZ",
          "content": {
            "background": "3.jpg",
            "label": "yes"
          }
        },
        {
          "bitcoin_address": "mo9GU4LeiKC4fWdNZfPYirK2qzJnS3urYX",
          "content": {
            "background": "2.jpg",
            "label": "no"
          }
        }
      ],
      "state": "preparing",
      "tags": [
        {
          "content": {
            "translates": {
              "en": {
                "display_name": "science"
              },
              "ru": {
                "display_name": "\u043d\u0430\u0443\u043a\u0430"
              }
            }
          },
          "name": "science"
        },
        {
          "content": {
            "translates": {
              "en": {
                "display_name": "politics"
              },
              "ru": {
                "display_name": "\u043f\u043e\u043b\u0438\u0442\u0438\u043a\u0430"
              }
            }
          },
          "name": "politics"
        }
      ]
    }
  ],
  "status": "ok"
}
```

#### Errors
```unknown_language_error```, ```nonexistent_entity_error```

## <a name="edit-event"/> Edit event
```POST /api/v1/event/<int:event_id>/```

#### Content
```json
{
  "state": "<new_state>",
  "tags": ["<new_tag_1", "<new_tag_2>"]
}
```

#### Parameters
```event_id``` - language of translations
```new_state``` - one of the following state: preparing, ongoing, holding, clearing, ended, deleted

#### Errors
```nonexistent_entity_error```, ```invalid_state_transition_error```

## <a name="create-new-tag"/> Create new tag
```POST /api/v1/tag/```

#### Headers

```Content-Type: "application/json"```

#### Content
```json
{
  "name": "science",
  "content": {
    "translates": {
      "ru": {
        "display_name": "наука"
      },
      "en": {
        "display_name": "science"
      }
    }
  }
}
```

#### Errors
```validation_error```

## <a name="edit-tag"/> Edit tag
```POST /api/v1/tag/<string:tag_name>```

#### Headers
```Content-Type: "application/json"```

#### Parameters
```tag_name``` - tag name

#### Content
```json
{
  "content": {
    "translates": {
      "ru": {
        "display_name": "наука"
      },
      "en": {
        "display_name": "science"
      }
    }
  }
}
```

#### Errors
```impossible_bro_error```, ```nonexistent_entity_error```

## <a name="delete-tag"/> Delete tag
```DELETE /api/v1/tag/<string:tag_name>```

#### Parameters
```tag_name``` - tag name

#### Errors
```impossible_bro_error```, ```nonexistent_entity_error```

## <a name="get-tags"/> Get tags
```GET /api/v1/tag/?lang=<string:lang>&raw=<int:raw>```

#### Parameters
```lang``` - language of translations

```raw``` - if 1 then get data without translation substitutions

#### Response
```json
{
  "status": "ok",
  "tags": [
    {
      "content": {
        "translates": {
          "en": {
            "display_name": "science"
          },
          "ru": {
            "display_name": "\u043d\u0430\u0443\u043a\u0430"
          }
        }
      },
      "name": "science"
    },
    {
      "content": {
        "translates": {
          "en": {
            "display_name": "politics"
          },
          "ru": {
            "display_name": "\u043f\u043e\u043b\u0438\u0442\u0438\u043a\u0430"
          }
        }
      },
      "name": "politics"
    }
  ]
}
```
