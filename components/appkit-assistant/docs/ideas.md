# Render information with a dedicated UI

"Action" classes, e.g. something like

```python
class Calender(AssitantAction):
   name: str
   description: str
   parameters: list[dict]

   def __init__(self):
      name = "showCalendarMeeting"
      description = "Displays calendar meeting information"
      parameters = [
        {
            name: "date",
            type: "string",
            description: "Meeting date (YYYY-MM-DD)",
            required: true
        },
        {
            name: "time",
            type: "string",
            description: "Meeting time (HH:mm)",
            required: true
        },
        {
            name: "meetingName",
            type: "string",
            description: "Name of the meeting",
            required: false
        }
    ]

    def render(status, **kwargs):
       if status == Status.LOADING:
          return loading_view()
       else:
          return calendar_entry(**kwargs)
```

## Next Actions

```python
class Suggestion(AssitantAction):
   name: str
   description: str
   parameters: list[dict]

   def __init__(self):
      name = "showSuggestion"
      description = "Displays suggestions"
      parameters = [
        {
            name: "suggestion",
            type: "string",
            description: "Suggestion what how to continue or what to ask next",
            required: false
        }
    ]

    def render(status, **kwargs):
       if status == Status.LOADING:
          return loading_view()
       else:
          return render_suggestion(**kwargs)
```
