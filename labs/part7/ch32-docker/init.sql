CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS course_vectors (
  id bigserial PRIMARY KEY,
  label text NOT NULL,
  embedding vector(3) NOT NULL
);
CREATE INDEX IF NOT EXISTS course_vectors_embedding_hnsw
  ON course_vectors USING hnsw (embedding vector_l2_ops);
INSERT INTO course_vectors (label, embedding)
SELECT 'docker lesson', '[0.1,0.2,0.3]'
WHERE NOT EXISTS (SELECT 1 FROM course_vectors);
