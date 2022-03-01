-- MENAMPILKAN SEMUA BARIS DAN KOLOL
SELECT * FROM teachers

-- MENAMPILKAN first_name, school, salary
SELECT first_name, school, salary FROM teachers;

-- MENGHITUNG JUMLAH GURU
SELECT COUNT(*) FROM teachers;

-- MENGURUTKAN GURU BERDASARKAN first_name
SELECT first_name, school, salary 
FROM teachers
ORDER BY first_name ASC;

-- MENAMPILKAN GURU YG MENGAJAR DI MIT
SELECT *
FROM teachers
WHERE school='MIT';

-- MENAMPILKAN GURU YG MENGAJAR DI MIT DAN DALARY>40000
SELECT *
FROM teachers
WHERE school='MIT' AND salary>40000;

-- MENAMPILKAN GURU YG MENGAJAR DI MIT atau DI HARVARD
SELECT *
FROM teachers
WHERE school='MIT' OR school='Harvard University';

-- ATAUU
SELECT *
FROM teachers
WHERE school IN ('MIT', 'Harvard University');

-- MENCARI UNIQUE SCHOOL
SELECT DISTINCT school
FROM teachers;

-- MENCARI JUMLAH UNIQUE SCHOOL
SELECT COUNT(DISTINCT school)
FROM teachers;

