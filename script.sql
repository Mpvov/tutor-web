USE tutor_system;
-- Disable foreign key checks to allow truncating tables
SET FOREIGN_KEY_CHECKS = 0;

-- Optional: Clear existing data to avoid duplicates
TRUNCATE TABLE appointments;
TRUNCATE TABLE time_slots;
TRUNCATE TABLE registrations;
TRUNCATE TABLE programs;
TRUNCATE TABLE users;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- ==========================================
-- 1. INSERT USERS
-- Password is hardcoded to be the same as 'mssv' for testing simplicity
-- ==========================================
INSERT INTO users (id, mssv, password, ho_ten, role) VALUES 
-- Students
(1, '2310001', '2310001', 'Nguyễn Văn An (Student)', 'student'),
(2, '2310002', '2310002', 'Trần Thị Bình (Student)', 'student'),
(3, '2310003', '2310003', 'Lê Văn Cường (Student)', 'student'),

-- Tutors
(4, '2010001', '2010001', 'Phạm Minh Đức (Tutor)', 'tutor'),
(5, '2010002', '2010002', 'Hoàng Thị Dung (Tutor)', 'tutor'),

-- Admin
(6, 'admin', 'admin', 'System Administrator', 'admin'),

-- Coordinator
(7, 'coord', 'coord', 'Lê Đình Thuận (Coordinator)', 'coordinator');


-- ==========================================
-- 2. INSERT PROGRAMS
-- ==========================================
INSERT INTO programs (id, name, semester, status) VALUES 
(1, 'Chương trình tutor HK2', 'HK2 2025-2026', 'open'),
(2, 'Chương trình tutor HK1', 'HK1 2025-2026', 'closed'),
(3, 'Chương trình tutor HK2', 'HK2 2024-2025', 'closed');


-- ==========================================
-- 3. INSERT REGISTRATIONS
-- Linking Students (IDs 1, 2, 3) to Programs (IDs 1, 2, 4)
-- ==========================================
INSERT INTO registrations (student_id, program_id) VALUES 
(1, 1), -- Student An registers for Đại Cương
(1, 2), -- Student An registers for C++
(2, 1), -- Student Bình registers for Đại Cương
(3, 4); -- Student Cường registers for Vật Lý


-- ==========================================
-- 4. INSERT TIME SLOTS
-- Creating slots for Tutors (IDs 4, 5)
-- Note: Dates are hardcoded for late 2025 to ensure they appear as "upcoming"
-- ==========================================
INSERT INTO time_slots (id, tutor_id, start_time, end_time, is_booked) VALUES 
-- Slots for Tutor Đức (ID 4)
(1, 4, '2025-12-01 08:00:00', '2025-12-01 09:00:00', 1), -- Booked
(2, 4, '2025-12-01 09:00:00', '2025-12-01 10:00:00', 0), -- Free
(3, 4, '2025-12-02 14:00:00', '2025-12-02 15:00:00', 0), -- Free

-- Slots for Tutor Dung (ID 5)
(4, 5, '2025-12-03 08:00:00', '2025-12-03 09:00:00', 0), -- Free
(5, 5, '2025-12-03 10:00:00', '2025-12-03 11:00:00', 1); -- Booked


-- ==========================================
-- 5. INSERT APPOINTMENTS
-- Linking Students to the 'Booked' Time Slots (is_booked = 1)
-- ==========================================
INSERT INTO appointments (student_id, slot_id, status) VALUES 
-- Student An (ID 1) booked Tutor Đức (Slot ID 1)
(1, 1, 'confirmed'),

-- Student Bình (ID 2) booked Tutor Dung (Slot ID 5)
(2, 5, 'pending');