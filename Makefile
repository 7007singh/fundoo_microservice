ifeq ($(OS), Windows_NT)
include .env
init:
	@pip install -r requirements.txt

run_user:
	@uvicorn main:user_app --port ${USER_PORT} --reload

run_note:
	@uvicorn main:note_app --port ${NOTE_PORT} --reload

endif