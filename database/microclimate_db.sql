-- microclimate_db schema

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `measurements` (
  `id` int(11) NOT NULL,
  `sensor_id` varchar(50) NOT NULL,
  `temperature` decimal(5,2) DEFAULT NULL,
  `humidity` decimal(5,2) DEFAULT NULL,
  `co2` int(11) DEFAULT NULL,
  `comfort_score` decimal(5,2) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `measurements` (`id`, `sensor_id`, `temperature`, `humidity`, `co2`, `comfort_score`, `timestamp`) VALUES
(1, 'Test_1', 22.50, 45.00, 800, 0, '2026-03-21 18:50:40');

ALTER TABLE `measurements`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `measurements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

COMMIT;

-- Migration for an existing database that already has comfort_score as INT:
-- ALTER TABLE `measurements` MODIFY `comfort_score` DECIMAL(5,2) DEFAULT NULL;
