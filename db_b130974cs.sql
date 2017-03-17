-- phpMyAdmin SQL Dump
-- version 4.6.6deb1+deb.cihar.com~trusty.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 17, 2017 at 04:41 PM
-- Server version: 5.5.54-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_b130974cs`
--

-- --------------------------------------------------------

--
-- Table structure for table `COMMITTEE`
--

CREATE TABLE `COMMITTEE` (
  `com_id` int(11) NOT NULL,
  `com_name` varchar(45) NOT NULL,
  `com_head_id` int(11) NOT NULL,
  `com_strength` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `COMMITTEE`
--

INSERT INTO `COMMITTEE` (`com_id`, `com_name`, `com_head_id`, `com_strength`) VALUES
(1, 'Mechanical', 1, 3),
(2, 'General', 2, 3),
(3, 'Workshops', 3, 3),
(4, 'Civil', 4, 3),
(5, 'Computer Science', 5, 3),
(6, 'Cultural', 6, 3);

-- --------------------------------------------------------

--
-- Table structure for table `EVENT`
--

CREATE TABLE `EVENT` (
  `event_id` int(11) NOT NULL,
  `event_name` varchar(45) NOT NULL,
  `event_com_id` int(11) NOT NULL,
  `event_mgr_id` int(11) NOT NULL,
  `event_date` date NOT NULL,
  `event_location` varchar(45) NOT NULL,
  `winner_team_id` int(11) DEFAULT NULL,
  `num_participants` int(11) DEFAULT '0',
  `event_description` varchar(2000) DEFAULT NULL,
  `participants_req` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `EVENT`
--

INSERT INTO `EVENT` (`event_id`, `event_name`, `event_com_id`, `event_mgr_id`, `event_date`, `event_location`, `winner_team_id`, `num_participants`, `event_description`, `participants_req`) VALUES
(1, 'Robot Circuit Race', 1, 1, '2015-11-22', 'ELHC', NULL, 1, 'Come onto to the race track filled with the unexpected as Tathva\'15 presents to you Robot Race.See if the robot of yours has what it takes to withstand this test of speed, skill and endurance. \n\n ', 1),
(2, 'Collision Course', 1, 2, '2015-11-22', 'Aryabhatta hall', 25, 1, 'Experience the spine chilling battle of mean robots designed solely for one purpose. Destruction!!', 1),
(3, 'Blueprint', 4, 3, '2015-11-22', 'MB', 25, 0, 'Blueprint is a core paper presentation where all the ingenious minds out there can showcase their immense knowledge on creating extravagant modern structures.', 1),
(4, 'Counter Strike', 5, 4, '2015-11-22', 'Computer Centre', NULL, 3, 'Moving Out...Affirmative!!\nTest your gaming skills to the next level with another CS 1.6 tournament for you to win.\n', 4),
(5, 'Shutterbugs', 2, 5, '2015-11-22', 'Rajpath', NULL, 0, 'Let the photos do the talking! Capture the experiences and visions that inspire you, and let that inspiration run free.So, gear up, get ready and show the world your true perspective.', 1),
(6, 'Sports Quiz', 2, 6, '2015-11-22', 'NLHC', NULL, 1, 'Is the sports category your quizzing forte? If yes then brace yourself for the ultimate test of your prowess. ', 1),
(7, 'Linkage', 4, 7, '2015-11-23', 'MB', NULL, 0, 'Use ice cream sticks to create a truss bridge.', 2),
(8, 'Treasure Hunt', 2, 8, '2015-11-23', 'Center Circle', NULL, 1, 'Extraordinary things are always hiding in places, people usually don’t think to look. But, do you!?\nTest it out at treasure hunt!', 4),
(9, 'Coder Combat', 5, 9, '2015-11-23', 'SSL', NULL, 1, 'Are you an ardent programmer? Do you believe you can model any real world problem into a program and solve it? If so we assure you that this is one competition where you can prove yourselves.', 1),
(10, 'Board Room', 2, 10, '2015-11-23', 'NLHC', NULL, 0, 'This is an event for all those who have a flair to sell anything under the sky.\n This is a platform where you can demonstrate how innovative and imaginative you can be and how you can convince buyers out there.\n', 1),
(11, 'Hacking Workshop', 3, 11, '2015-11-23', 'Robotics Lab', NULL, 2, 'Do You Think That Your Facebook Password\'s Are Safe? How Do You Know If The Transactions That You Do Are Safe Or Not? What Are You Going To Do Then? Have You Ever Thought About It? Well No Need To Worry!Learn ethical hacking in this event.', 1),
(12, 'Photography Workshop', 3, 12, '2015-11-24', 'MB', NULL, 1, 'Bring out the photographer in you by enrolling for a 2-day workshop conducted by established photographers in and around Kerala.', 1),
(13, 'Martial Arts Workshop', 3, 13, '2015-11-24', 'Football Ground', NULL, 1, 'Master the art of karate by participating in a 3-day workshop conducted by black belt Mr. Xang Wu.', 1),
(14, 'Street Play', 6, 14, '2015-11-24', 'Auditorium', NULL, 0, 'Teams are given a topic on which a street play should be performed in the given time limit.', 8),
(15, 'Mime', 6, 15, '2015-11-24', 'Auditorium', NULL, 0, 'Perform as a mime team enacting a given topic in a specific time limit.', 8),
(16, 'Dumb Charades', 2, 16, '2015-11-24', 'MB', NULL, 0, 'Battle your acting skills out in the classic game of Dumb charades.', 3),
(17, 'Antakshri', 2, 17, '2015-11-24', 'NLHC', NULL, 0, 'Another classic game with a few twists to let your hearts go singing.', 4),
(18, 'Mr. and Ms. Personality', 6, 18, '2015-11-24', 'OAT', NULL, 0, 'A series of tests to determine the ultimate personalities of the college.', 1),
(19, 'Fashion Show', 1, 1, '2015-11-22', 'OAT', NULL, 0, 'An event to design costumes and showcase the same on the ramp.', 1),
(20, 'Dance Wars', 2, 2, '2015-11-23', 'OAT', NULL, 0, 'Show what moves you got and set the stage on fire.', 8),
(21, 'Court Room', 3, 3, '2015-11-23', 'MB', NULL, 0, 'Enact real court room proceedings on a given topic.', 4);

-- --------------------------------------------------------

--
-- Table structure for table `MANAGING_TEAM`
--

CREATE TABLE `MANAGING_TEAM` (
  `member_id` int(11) NOT NULL,
  `member_name` varchar(45) NOT NULL,
  `member_com_id` int(11) NOT NULL,
  `password` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `MANAGING_TEAM`
--

INSERT INTO `MANAGING_TEAM` (`member_id`, `member_name`, `member_com_id`, `password`) VALUES
(1, 'Harshit', 1, 'hash123'),
(2, 'Anurag', 2, 'Anucar'),
(3, 'Nirant', 3, 'knpmg'),
(4, 'Ashwin', 4, 'ashwin'),
(5, 'Anshul', 5, 'anshul'),
(6, 'Bhupendra', 6, 'bhuppi'),
(7, 'Naman', 1, 'naman'),
(8, 'Nihal', 2, 'nihal'),
(9, 'Sreeja', 3, 'sreeja'),
(10, 'Reshmi', 4, 'reshmi'),
(11, 'Aakansha', 5, 'aakansha'),
(12, 'Vishal', 6, 'vishal'),
(13, 'Shreyas', 1, 'shreyas'),
(14, 'Nishreyas', 2, 'nishreyas'),
(15, 'Hari', 3, 'hari'),
(16, 'Bhageerath', 4, 'bhageerath'),
(17, 'Rohit', 5, 'rohit'),
(18, 'Sakar', 6, 'sakar');

-- --------------------------------------------------------

--
-- Table structure for table `PARTICIPANTS`
--

CREATE TABLE `PARTICIPANTS` (
  `name` varchar(40) NOT NULL,
  `part_id` int(10) NOT NULL,
  `contact` varchar(10) NOT NULL,
  `college` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `PARTICIPANTS`
--

INSERT INTO `PARTICIPANTS` (`name`, `part_id`, `contact`, `college`) VALUES
('ab', 1, '9567884834', 'sfsf'),
('ashwin', 2, '9009409934', 'nitc'),
('adhaj', 3, '1234567890', 'adhaj'),
('Anurag Naik', 4, '9567884834', 'Nit Calicut');

-- --------------------------------------------------------

--
-- Table structure for table `TEAM`
--

CREATE TABLE `TEAM` (
  `team_id` int(11) NOT NULL,
  `team_name` varchar(45) NOT NULL,
  `team_strength` int(11) DEFAULT '0',
  `team_event_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `TEAM`
--

INSERT INTO `TEAM` (`team_id`, `team_name`, `team_strength`, `team_event_id`) VALUES
(25, 'q', 1, 2),
(26, 'Anurag', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `TEAM_PART`
--

CREATE TABLE `TEAM_PART` (
  `team_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `TEAM_PART`
--

INSERT INTO `TEAM_PART` (`team_id`, `part_id`) VALUES
(25, 2),
(26, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `COMMITTEE`
--
ALTER TABLE `COMMITTEE`
  ADD PRIMARY KEY (`com_id`),
  ADD KEY `com_head_id_idx` (`com_head_id`),
  ADD KEY `com_head_id` (`com_head_id`),
  ADD KEY `com_id` (`com_id`),
  ADD KEY `com_id_2` (`com_id`);

--
-- Indexes for table `EVENT`
--
ALTER TABLE `EVENT`
  ADD PRIMARY KEY (`event_id`),
  ADD KEY `event_mgr_id_idx` (`event_mgr_id`),
  ADD KEY `event_com_idx` (`event_com_id`),
  ADD KEY `fk_EVENT_1_idx` (`winner_team_id`);

--
-- Indexes for table `MANAGING_TEAM`
--
ALTER TABLE `MANAGING_TEAM`
  ADD PRIMARY KEY (`member_id`),
  ADD KEY `member_com_id` (`member_com_id`);

--
-- Indexes for table `PARTICIPANTS`
--
ALTER TABLE `PARTICIPANTS`
  ADD PRIMARY KEY (`part_id`);

--
-- Indexes for table `TEAM`
--
ALTER TABLE `TEAM`
  ADD PRIMARY KEY (`team_id`),
  ADD KEY `team_event_id_idx` (`team_event_id`);

--
-- Indexes for table `TEAM_PART`
--
ALTER TABLE `TEAM_PART`
  ADD PRIMARY KEY (`team_id`,`part_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `EVENT`
--
ALTER TABLE `EVENT`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
--
-- AUTO_INCREMENT for table `MANAGING_TEAM`
--
ALTER TABLE `MANAGING_TEAM`
  MODIFY `member_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT for table `PARTICIPANTS`
--
ALTER TABLE `PARTICIPANTS`
  MODIFY `part_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `TEAM`
--
ALTER TABLE `TEAM`
  MODIFY `team_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `COMMITTEE`
--
ALTER TABLE `COMMITTEE`
  ADD CONSTRAINT `com_head_id` FOREIGN KEY (`com_head_id`) REFERENCES `MANAGING_TEAM` (`member_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `EVENT`
--
ALTER TABLE `EVENT`
  ADD CONSTRAINT `event_com_id` FOREIGN KEY (`event_com_id`) REFERENCES `COMMITTEE` (`com_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `event_mgr_id` FOREIGN KEY (`event_mgr_id`) REFERENCES `MANAGING_TEAM` (`member_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `winner_team_id` FOREIGN KEY (`winner_team_id`) REFERENCES `TEAM` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `MANAGING_TEAM`
--
ALTER TABLE `MANAGING_TEAM`
  ADD CONSTRAINT `member_com_id` FOREIGN KEY (`member_com_id`) REFERENCES `COMMITTEE` (`com_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `TEAM`
--
ALTER TABLE `TEAM`
  ADD CONSTRAINT `team_event_id` FOREIGN KEY (`team_event_id`) REFERENCES `EVENT` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
