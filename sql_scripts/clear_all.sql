-- Очистка всех таблиц
DELETE FROM appointments_workouts;
DELETE FROM trainers_workouts;
DELETE FROM appointments;
DELETE FROM clients;
DELETE FROM workouts;
DELETE FROM trainers;

-- Сброс автоинкремента
DELETE FROM sqlite_sequence;