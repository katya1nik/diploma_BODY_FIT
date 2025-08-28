-- Создание таблицы "Тренера"
CREATE TABLE IF NOT EXISTS trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT NOT NULL,
    name_of_training_session TEXT NOT NULL
);

-- Создание таблицы "Тренировки"
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_of_training_session TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT NOT NULL,
    description TEXT
);

-- Создание таблицы "Клиенты"
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    name_of_training_session TEXT NOT NULL
);

-- Создание таблицы "Запись на тренировки"
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trener_id INTEGER,
    name_of_training_session TEXT NOT NULL,
    FOREIGN KEY (trener_id) REFERENCES trainers(id)
);

-- Создание связующей таблицы тренеров и тренировок
CREATE TABLE IF NOT EXISTS trainers_workouts (
    trener_id INTEGER,
    workout_id INTEGER,
    PRIMARY KEY (trener_id, workout_id),
    FOREIGN KEY (trener_id) REFERENCES trainers(id),
    FOREIGN KEY (workout_id) REFERENCES workouts(id)
);

-- Создание связующей таблицы записей и тренировок
CREATE TABLE IF NOT EXISTS appointments_workouts (
    appointment_id INTEGER,
    workout_id INTEGER,
    PRIMARY KEY (appointment_id, workout_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
    FOREIGN KEY (workout_id) REFERENCES workouts(id)
);
