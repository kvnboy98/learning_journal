SELECT count(*)
FROM teachers;

-- JUMLAHANN
SELECT SUM(salary)
FROM teachers
WHERE school='MIT';

-- RATA-RATA
SELECT AVG(salary)
FROM teachers
WHERE school='MIT';

-- PEMBULATAN KEATAS
SELECT CEIL(AVG(salary))
FROM teachers
WHERE school='MIT';

-- PEMBULATAN KEBAWAH
SELECT FLOOR(AVG(salary))
FROM teachers
WHERE school='MIT';

-- MELIHAT NAMA DOSEN YANG NAMA DEPANYA BERAWALAN 'SAM'
SELECT *
FROM teachers
WHERE first_name LIKE 'Sam%'

-- MELIHAT JUMLAH DOSEN DISETIAP UNIV
SELECT school, COUNT(teachers.id)
FROM teachers
GROUP BY school

-- MELIHAT SALARY TERTINGGI DI SETIAP UNIV 
SELECT school, MAX(salary)
FROM teachers
GROUP BY school

-- CARI RATA2 SALARY DI SETIAP UNIV 
SELECT school, floor(AVG(salary)) as "rata-rata gaji"
FROM teachers
GROUP BY school

-- melihat dosen yg memiliki salary terendah di cambridge (SUB-QUERY)
SELECT *
FROM teachers
WHERE school="Cambridge University" and salary=(
  SELECT min(salary)
  FROM teachers
  WHERE school="Cambridge University")

-- pake ini juga bisa
SELECT *
FROM teachers
WHERE school LIKE 'Cambri%' and salary=(
	SELECT min(salary)
	FROM teachers
	WHERE school LIKE 'Cambri%');

-- menampilkan setiap dosen yg memiliki gaji tertinggi di setiap univ
SELECT id, first_name, last_name, school, salary
FROM teachers
WHERE (school, salary) IN (
  SELECT school, MAX(salary)
  from teachers
  GROUP BY school);
  
-- melihat dosen siapa yang mengajar apa
SELECT *
from teachers
JOIN courses on teachers.id=courses.teachers_id;

-- menghitung jumlah mata kuliah yang diajarkan oleh para dosen
SELECT teachers.id, teachers.first_name, teachers.last_name, COUNT(courses.id)
FROM teachers
join courses on teachers.id=courses.teachers_id
GROUP BY teachers.id

-- menghitung jumlah total student masing-masing dosen
SELECT teachers.id, teachers.first_name, teachers.last_name, SUM(courses.total_students) as 'jumlah_siswa'
FROM teachers
join courses on teachers.id=courses.teachers_id
GROUP BY teachers.id
ORDER by jumlah_siswa DESC;