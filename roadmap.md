# Project Roadmap for izdivac25

## Phase 1: Stabilize and Complete the Questionnaire (1-2 Weeks)

**Goal**: Get the full questionnaire working with your planned questions, ensuring a smooth user experience and reliable data collection.

- ### 1. Expand Models (3-5 Days)

  - **Task**: Update `questions/models.py` with new structure:
    - Create new `AnalyzableData` model linked to `UserSession` for quantitative match criteria:

      ```python
      class AnalyzableData(models.Model):
          session = models.OneToOneField(UserSession, on_delete=models.CASCADE)
          age_min = models.IntegerField()
          age_max = models.IntegerField()
          height_min = models.IntegerField()
          height_max = models.IntegerField()
          zodiac_sign = models.CharField(max_length=20)
          romance_score = models.FloatField()
      ```

    - Keep `Answer` model for free-text and choice-based responses
    - Add JSONField to `Answer` for complex open-ended responses
  - **Why**: Separates analyzable match criteria from qualitative responses for better organization and query efficiency
  - **Priority**: *High* (core to your app)

- ### 2. Enhance Forms (3-5 Days)

  - **Task**: Update `AnswerForm` in `questions/forms.py` to dynamically render new question types:
    - Range inputs (e.g., `<input type="number">` for age/height)
    - Multi-line text for open-ended questions with lists (e.g., "En Sevdiğin Filmler")
    - Predefined choices for single/multiple-select questions (e.g., "İlişki Durumu" options: ciddi/fwb/ons)
  - **Why**: Your form currently supports 3-4 test questions; this scales it to your full list
  - **Priority**: *High*

- ### 3. Populate Questions (2-3 Days)

  - **Task**: Add all your planned questions to the `Question` model via the Django admin or a data migration:
    - Example: `Question(text="Yaş Aralığı", q_type="range", section=2)`
    - Categorize by section (1-5 as per your list)
  - **Why**: You need the full dataset to test and collect meaningful responses
  - **Priority**: *High*

- ### 4. Fix Templates (2 Days)

  - **Task**:
    - Update `answer_form.html` to handle new input types (e.g., number fields, better styling for lists)
    - Add the `matching_code` to `success.html` so users can note it down (you'll use it to identify them)
  - **Why**: Improves usability and gives users a reference for you to contact them
  - **Priority**: *Medium*

**Milestone**: By the end of Phase 1, users can complete the full questionnaire, and all responses are stored correctly.

---

## Phase 2: Build Matching Tools (1-2 Weeks)

**Goal**: Create admin tools to analyze responses and generate matches, since you'll handle contacting users manually.

- ### 5. Basic Matching Logic (3-5 Days)

  - **Task**: Add a simple matching function in `questions/views.py` for `view_all_responses`:
    - Compare analyzable fields from `AnalyzableData` model
    - Example: If User A wants `age_range: 20-25` and User B is 23, flag as a potential match
  - **Why**: Automates part of your manual process, even if basic (e.g., filter by hard requirements)
  - **Priority**: *High* (core to your matchmaking)

- ### 6. Enhance Admin View (3-5 Days)

  - **Task**: Update `admin_view_responses.html` and its view:
    - Add filters (e.g., by section, question type, or specific answers like "Ciddi İlişki")
    - Display match suggestions based on the logic above
    - Color-code analyzable (e.g., blue) vs. non-analyzable (e.g., yellow) responses (you've already started this)
  - **Why**: Makes it easier for you to review and pair people
  - **Priority**: *High*

- ### 7. Export Improvements (2 Days)

  - **Task**: Enhance CSV/JSON exports in `admin_view_responses.html`:
    - Include `matching_code` and contact info in exports
    - Structure CSV columns by question for easier analysis in Excel/Google Sheets
  - **Why**: Simplifies your offline matching workflow
  - **Priority**: *Medium*

**Milestone**: You can view all responses, filter them, and see basic match suggestions in the admin interface.

---

## Phase 3: Polish and Test (1 Week)

**Goal**: Ensure the app is reliable and user-friendly for your friends, with no major bugs.

- ### 8. Security Tweaks (1-2 Days)

  - **Task**:
    - Replace the hardcoded admin password (`'123'`) with an environment variable (e.g., `os.environ.get('ADMIN_PASS')`)
    - Turn off `DEBUG = True` for deployment and set `ALLOWED_HOSTS`
  - **Why**: Basic protection since this is for friends, not public, but still good practice
  - **Priority**: *Medium*

- ### 9. User Experience (2 Days)

  - **Task**:
    - Add a welcome page (e.g., at `start_questionnaire`) explaining the process ("Fill this out, I'll contact you with matches!")
    - Improve error handling in `submit_answer` (e.g., show "Please fill this field" to users, not just log it)
  - **Why**: Makes it friendlier and clearer for your target audience
  - **Priority**: *Medium*

- ### 10. Testing (2-3 Days)

  - **Task**:
    - Test with 5-10 dummy responses (use your friends' profiles as templates)
    - Check all question types (single, multiple, open-ended) save correctly
    - Verify matching suggestions and exports work
  - **Why**: Ensures everything works before rollout
  - **Priority**: *High*

**Milestone**: The app is ready to deploy and use with your friends.

---

## Phase 4: Deploy and Collect Responses (Ongoing)

**Goal**: Get it live, collect data, and start matchmaking.

- ### 11. Deployment (1-2 Days)

  - **Task**:
    - Host on a free platform (e.g., Heroku, Render) with SQLite for simplicity
    - Share the URL with your friends
  - **Why**: Gets it out of local development and into their hands
  - **Priority**: *High*

- ### 12. Matchmaking Workflow (Ongoing)

  - **Task**:
    - Use the admin view to review responses
    - Manually refine matches based on non-analyzable data (e.g., "Celebrity Crush" vibes)
    - Contact users via their provided info (IG/email) with their `matching_code` as reference
  - **Why**: This is your endgame—connecting your friends!
  - **Priority**: *High*

**Milestone**: Friends are filling it out, and you're making matches.

---

## Timeline Summary

- **Phase 1**: 1-2 weeks (core questionnaire)
- **Phase 2**: 1-2 weeks (matching tools)
- **Phase 3**: 1 week (polish and test)
- **Phase 4**: 1-2 days setup + ongoing use
- **Total**: 4-7 weeks to a working app, depending on your pace.

## Priorities

- **High**: Questionnaire completion, basic matching, testing, deployment.
- **Medium**: UI polish, export enhancements, basic security.
- **Low**: Scalability (not needed per your specs).

## Notes

- **No Auth**: Your Google Docs inspiration is already in play with session-based tracking. No changes needed!
- **Manual Contact**: Since users don't see matches, the `matching_code` and contact info are key—ensure they're prominent in the success page and exports.
- **Small Scale**: SQLite and minimal security are fine for your friends-only use case.

---

## Next Steps

Start with **Phase 1, Task 1**: Implement the new `AnalyzableData` model structure. Want me to draft the model updates in `questions/models.py`?
