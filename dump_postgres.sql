-- BEGIN TRANSACTION;
BEGIN;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    hash VARCHAR NOT NULL
);

-- INSERT INTO users (id, username, email, hash) VALUES
-- (1, 'sumitkumar', '2003.sumit.kumar@gmail.com', 'scrypt:32768:8:1$QXERYL3Yqf0dK9uj$4784bdc7fffaedfa1965b371516a33ead86e78b8c8ee6c3c18e46b6440b0530233a3bebe9d72efc422f10a9c010e873e7f8fdd1ea64060466e27f7c225cec92f'),
-- (2, 'testuser', 'test@gmail.com', 'scrypt:32768:8:1$T2IPZV7rj6TtZeXq$a13b05f40b05cdd99e17e6c9c014cb858be90fbb20ff7e3931390a0b5c3e0906cf2edc51dbbfb028df36b3cea6e15e932eee4ce31f5ceab50052cc9e16d030a6'),
-- (3, 'iamsumitkr', 'test@gmail.com', 'scrypt:32768:8:1$twMbePxb5DcF0kjr$54b6c5187a55fbc44b3756d599cefca0979968d9686f3aeaa3e65ff1e235f63742fdb56bde0b50cc4222f197988c304af7afd01e3b9f41168342b6964f4bed3f');

CREATE TABLE watchlist (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id),
    name VARCHAR NOT NULL,
    rating INT NOT NULL,
    review TEXT
);

-- INSERT INTO watchlist (id, userid, name, rating, review) VALUES
-- (19, 1, 'Sapne VS Everyone', 5, 'Best show from TVF, really good story, will keep you hooked till the end'),
-- (20, 1, 'Oppenheimer', 3, 'Samajh nahi aaya zyada kuch'),
-- (21, 2, 'test1', 5, 'review'),
-- (22, 3, 'Oppenheimer', 4, 'nice movie'),
-- (23, 1, 'Pirates of the Carribean 1', 5, 'good movie');

-- COMMIT;
COMMIT;
