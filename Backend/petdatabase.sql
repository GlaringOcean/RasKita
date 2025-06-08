-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 07 Jun 2025 pada 20.03
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `petdatabase`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `catbreeds`
--

CREATE TABLE `catbreeds` (
  `cat_id` int(11) NOT NULL,
  `breed_name` varchar(50) NOT NULL,
  `height_male_min` decimal(4,1) NOT NULL,
  `height_male_max` decimal(4,1) NOT NULL,
  `height_female_min` decimal(4,1) NOT NULL,
  `height_female_max` decimal(4,1) NOT NULL,
  `weight_male_min` decimal(5,1) NOT NULL,
  `weight_male_max` decimal(5,1) NOT NULL,
  `weight_female_min` decimal(5,1) NOT NULL,
  `weight_female_max` decimal(5,1) NOT NULL,
  `life_expectancy_min` int(11) NOT NULL,
  `life_expectancy_max` int(11) NOT NULL,
  `characteristics` text NOT NULL,
  `exercise_needs` text NOT NULL,
  `grooming_requirements` text NOT NULL,
  `health_considerations` text NOT NULL,
  `diet_nutrition` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ;

--
-- Dumping data untuk tabel `catbreeds`
--

INSERT INTO `catbreeds` (`cat_id`, `breed_name`, `height_male_min`, `height_male_max`, `height_female_min`, `height_female_max`, `weight_male_min`, `weight_male_max`, `weight_female_min`, `weight_female_max`, `life_expectancy_min`, `life_expectancy_max`, `characteristics`, `exercise_needs`, `grooming_requirements`, `health_considerations`, `diet_nutrition`, `created_at`, `updated_at`) VALUES
(1, 'Abyssinian', 8.0, 10.0, 8.0, 10.0, 7.0, 12.0, 6.0, 9.0, 14, 17, 'Friendly, interactive, animated, active, and playful', 'Requires ample playtime and mental stimulation', 'Minimal grooming due to short coat; regular brushing helps maintain coat health', 'Regular veterinary check-ups are important', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(2, 'American Bobtail', 9.0, 10.0, 9.0, 10.0, 16.0, 16.0, 16.0, 16.0, 15, 15, 'Affectionate, sociable, playful, adaptable, and intelligent', 'Needs daily play; enjoys interactive toys', 'Moderate grooming depending on coat type (short or long)', 'Some risk of spinal issues due to short tail; otherwise generally healthy', 'Balanced diet with sufficient protein; monitor for overeating', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(3, 'American Shorthair', 8.0, 10.0, 8.0, 10.0, 11.0, 15.0, 6.0, 12.0, 15, 20, 'Gentle, affectionate, playful, easygoing, curious', 'Moderate exercise; likes routine play', 'Low grooming; weekly brushing maintains coat', 'Risk of hypertrophic cardiomyopathy', 'Portion-controlled diet; avoid obesity with proper feeding schedule', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(4, 'Bengal', 8.0, 10.0, 8.0, 10.0, 9.0, 15.0, 6.0, 12.0, 12, 16, 'Affectionate, energetic, animated', 'High – Bengals are extremely athletic and require ample space and opportunities for exercise', 'Low – Their short coat requires minimal grooming; regular brushing helps maintain coat health', 'Generally healthy but may be prone to certain genetic conditions; regular veterinary check-ups are essential', 'A balanced, high-protein diet is recommended; monitor food intake to prevent obesity', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(5, 'British Shorthair', 12.0, 14.0, 12.0, 14.0, 10.0, 16.0, 8.0, 11.0, 12, 16, 'Affectionate, easy-going, and calm', 'Moderate; enjoys play but not overly active', 'Weekly brushing needed due to dense double coat', 'Prone to obesity and hypertrophic cardiomyopathy', 'Needs portion control and balanced diet to maintain healthy weight', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(6, 'Maine Coon', 10.0, 16.0, 10.0, 16.0, 9.0, 20.0, 9.0, 20.0, 12, 15, 'Amiable, gentle and dog-like', 'Moderate; loves to play and climb', 'High – long coat requires frequent brushing', 'Risk of hypertrophic cardiomyopathy and hip dysplasia', 'Needs protein-rich diet; monitor weight due to size', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(7, 'Persian', 14.0, 17.0, 14.0, 17.0, 7.0, 12.0, 7.0, 12.0, 8, 20, 'Sweet, gentle, affectionate', 'Low to moderate; enjoys gentle play', 'High; daily brushing needed to prevent matting', 'Susceptible to respiratory issues and polycystic kidney disease', 'High-protein diet with animal-based proteins to maintain coat and muscle health', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(8, 'Ragdoll', 40.0, 40.0, 40.0, 40.0, 15.0, 20.0, 10.0, 15.0, 17, 17, 'Friendly, easygoing, cuddly, social', 'Moderate; enjoys interactive play but generally calm', 'Moderate; regular brushing to manage shedding', 'Prone to hypertrophic cardiomyopathy and obesity', 'High-quality protein diet to support their large frame and prevent weight gain', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(9, 'Siamese', 24.0, 24.0, 24.0, 24.0, 8.0, 12.0, 5.0, 8.0, 10, 20, 'Sociable, friendly, vocal', 'High; very active and enjoys interactive play', 'Low; short coat requires minimal grooming', 'May have genetic predispositions to certain health issues; regular vet check-ups recommended', 'Protein-rich, meat-heavy diet to support their active lifestyle', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(10, 'Sphynx', 13.0, 15.0, 13.0, 15.0, 8.0, 12.0, 7.0, 10.0, 7, 15, 'Playful, affectionate, friendly, energetic, loving', 'High; energetic and playful', 'High; requires regular bathing to remove oil buildup on the skin', 'Sensitive to temperature changes; prone to skin conditions', 'High-quality diet to meet energy needs and support skin health', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(11, 'Birman', 8.0, 10.0, 8.0, 10.0, 7.0, 14.0, 7.0, 14.0, 9, 15, 'Gentle, quiet, and loving', 'Moderate – Birmans enjoy playtime and interactive toys but are generally calm', 'Moderate – Their silky, long coat requires regular brushing to prevent matting', 'Generally healthy; regular veterinary visits help maintain overall well-being', 'Provide a balanced diet; monitor weight to prevent obesity', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(12, 'Bombay', 9.0, 11.0, 9.0, 11.0, 15.0, 15.0, 15.0, 15.0, 12, 18, 'Affectionate, sociable, needy, playful', 'Moderate – Bombays are active and enjoy daily play sessions', 'Low – Their short, sleek coat requires minimal grooming; weekly brushing is sufficient', 'Generally healthy but may be prone to heart and respiratory issues; regular veterinary check-ups are important', 'Provide a balanced diet; monitor food intake to prevent obesity', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(13, 'Calico', 9.0, 10.0, 9.0, 10.0, 12.0, 12.0, 12.0, 12.0, 15, 15, 'Sassy, spunky, bold, affectionate, independent, loyal', 'Varies – generally moderate play needed', 'Minimal to moderate depending on coat length', 'Generally healthy; females only (males are rare and sterile)', 'Balanced meals; tailor diet to specific breed', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(14, 'Egyptian Mau', 8.0, 10.0, 8.0, 10.0, 6.0, 14.0, 6.0, 14.0, 12, 15, 'Playful, active, devoted, loyal, alert, affectionate on their own terms', 'High - very athletic; loves to climb and run', 'Minimal grooming; short, sleek coat', 'Prone to heart issues; regular checkups needed', 'High-quality protein-rich diet recommended', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(15, 'Munchkin', 6.0, 9.0, 6.0, 9.0, 9.0, 9.0, 9.0, 9.0, 15, 15, 'Friendly, sociable, playful, and energetic', 'Moderate – active but limited by short legs', 'Regular brushing to keep coat clean and reduce shedding; check nails and ears routinely', 'Risk of spinal and joint issues', 'Balanced diet important; dont overfeed to avoid pressure on limbs', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(16, 'Norwegian Forest', 36.0, 36.0, 36.0, 36.0, 12.0, 18.0, 8.0, 12.0, 13, 16, 'Friendly, interactive, independent, adventurous', 'Moderate to high; enjoys climbing and interactive play', 'Requires weekly brushing; more frequent during shedding seasons', 'Prone to hypertrophic cardiomyopathy and hip dysplasia', 'High-protein diet with healthy fats to support their dense coat and energy needs', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(17, 'Ocicat', 24.0, 24.0, 24.0, 24.0, 10.0, 12.0, 8.0, 10.0, 15, 15, 'Affectionate, social, playful, vocal', 'High; active and playful, benefits from interactive toys', 'Low; short coat requires minimal maintenance', 'Generally healthy; regular dental care recommended', 'Species-appropriate, high-protein diet; grain-free options preferred', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(18, 'Russian Blue', 24.0, 24.0, 24.0, 24.0, 12.0, 12.0, 12.0, 12.0, 10, 20, 'Friendly, intelligent but aloof, reclusive to stranger', 'Moderate; enjoys play but can be reserved', 'Low; dense coat requires minimal grooming', 'Generally healthy; monitor for obesity', 'Balanced diet with controlled portions to prevent weight gain', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(19, 'Scottish Fold', 30.0, 30.0, 30.0, 30.0, 7.0, 11.0, 7.0, 11.0, 11, 14, 'Affectionate, sociable but not demanding', 'Moderate; playful but not overly active', 'Low; weekly brushing suffices', 'Prone to osteochondrodysplasia affecting cartilage and bone development', 'Complete and balanced diet appropriate for their life stage', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(20, 'Tortoiseshell', 9.0, 10.0, 9.0, 10.0, 6.0, 12.0, 6.0, 12.0, 12, 16, 'Spirited, independent, vocal, loyal, sometimes feisty', 'Varies; generally benefits from regular play to maintain health', 'Depends on coat length; regular brushing recommended', 'No specific health issues tied to coat pattern; general cat health maintenance applies', 'Balanced diet appropriate for their specific breed and life stage', '2025-06-07 17:44:12', '2025-06-07 17:44:12'),
(21, 'Tuxedo', 36.0, 36.0, 36.0, 36.0, 18.0, 18.0, 18.0, 18.0, 20, 20, 'Varies with breed', 'Varies; regular play helps maintain a healthy weight', 'Depends on underlying breed; generally low to moderate grooming needs', 'No specific health issues tied to coat pattern; monitor for common feline health concerns', 'Balanced and nutritious diet tailored to their specific breed and age', '2025-06-07 17:44:12', '2025-06-07 17:44:12');

-- --------------------------------------------------------

--
-- Struktur dari tabel `dogbreeds`
--

CREATE TABLE `dogbreeds` (
  `dog_id` int(11) NOT NULL,
  `breed_name` varchar(50) NOT NULL,
  `height_male_min` decimal(4,1) NOT NULL,
  `height_male_max` decimal(4,1) NOT NULL,
  `height_female_min` decimal(4,1) NOT NULL,
  `height_female_max` decimal(4,1) NOT NULL,
  `weight_male_min` decimal(5,1) NOT NULL,
  `weight_male_max` decimal(5,1) NOT NULL,
  `weight_female_min` decimal(5,1) NOT NULL,
  `weight_female_max` decimal(5,1) NOT NULL,
  `life_expectancy_min` int(11) NOT NULL,
  `life_expectancy_max` int(11) NOT NULL,
  `characteristics` text NOT NULL,
  `exercise_needs` text NOT NULL,
  `grooming_requirements` text NOT NULL,
  `health_considerations` text NOT NULL,
  `diet_nutrition` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ;

--
-- Dumping data untuk tabel `dogbreeds`
--

INSERT INTO `dogbreeds` (`dog_id`, `breed_name`, `height_male_min`, `height_male_max`, `height_female_min`, `height_female_max`, `weight_male_min`, `weight_male_max`, `weight_female_min`, `weight_female_max`, `life_expectancy_min`, `life_expectancy_max`, `characteristics`, `exercise_needs`, `grooming_requirements`, `health_considerations`, `diet_nutrition`, `created_at`, `updated_at`) VALUES
(1, 'Alaskan Malamute', 25.0, 25.0, 23.0, 23.0, 85.0, 85.0, 75.0, 75.0, 10, 14, 'Affectionate, Loyal, Playful, Dignified, Friendly, Devoted', 'High energy; needs daily vigorous exercise like hiking, running, or pulling sleds', 'Thick double coat needs frequent brushing, especially during shedding seasons. Bathe occasionally', 'Generally healthy but can have hip dysplasia and inherited diseases. Regular vet checks recommended', 'Feed high-quality dog food suited for large, active breeds. Monitor weight and avoid overfeeding', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(2, 'American Bulldog', 22.0, 25.0, 20.0, 23.0, 75.0, 100.0, 60.0, 80.0, 10, 12, 'Confident, Assertive, Affectionate, Loyal, Playful, Protective, Intelligent', 'Athletic; puppies need low-impact play, adults thrive with varied, daily activity. Not ideal for outdoor isolation', 'Low-maintenance—occasional baths, regular brushing, nail trims, ear cleaning, and teeth brushing. Seasonal shedding', 'Generally healthy; prone to hip/elbow issues. Regular vet checks and genetic screening recommended', 'Large-breed puppy food for 14 months; no extra calcium early. Adults need quality food with joint/muscle supplements', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(3, 'American Pit Bull Terrier', 18.0, 21.0, 17.0, 20.0, 35.0, 60.0, 30.0, 50.0, 12, 17, 'Confident, enthusiastic, friendly, intelligent, strong-willed', 'Requires regular exercise to maintain physical and mental health', 'Minimal grooming due to short coat', 'Prone to hip dysplasia and skin conditions; regular veterinary check-ups recommended', 'Balanced diet essential; consult a veterinarian for specific dietary need', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(4, 'Basset Hound', 15.0, 15.0, 15.0, 15.0, 40.0, 65.0, 40.0, 65.0, 12, 13, 'Charming, low-key, and sometimes stubborn', 'Regular exercise to prevent obesity and maintain health', 'Minimal grooming; regular ear cleaning is essential due to their long ears', 'Prone to certain health issues; regular veterinary check-ups are important', 'Balanced diet to prevent obesity; monitor food intake carefully', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(5, 'Beagle', 14.0, 16.0, 13.0, 15.0, 18.0, 25.0, 20.0, 23.0, 10, 15, 'Friendly, curious, and merry', 'Requires regular exercise to maintain health and prevent obesity', 'Minimal grooming due to short coat; regular ear cleaning is important', 'Prone to certain health issues; regular veterinary check-ups are important', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(6, 'Boxer', 22.5, 25.0, 21.0, 23.5, 65.0, 80.0, 50.0, 65.0, 10, 12, 'Bright, energetic, playful, loyal, affectionate', 'Requires regular exercise to maintain physical and mental health', 'Minimal grooming due to short coat; regular brushing helps maintain coat health', 'Prone to certain health issues; regular veterinary check-ups are important', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(7, 'Bulldog', 14.0, 15.0, 14.0, 15.0, 50.0, 50.0, 40.0, 40.0, 8, 10, 'Friendly, Courageous, Calm; Sweet, Devoted, Easygoing', 'Needs moderate activity like short walks; avoid heat and deep water due to breathing issues', 'Low-maintenance coat; regular brushing and wrinkle cleaning keep skin healthy', 'Prone to overheating and breathing problems; keep cool and visit the vet regularly', 'Balanced diet needed; watch portions to prevent obesity. Fresh water should always be available', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(8, 'Chihuahua', 6.0, 9.0, 6.0, 9.0, 6.0, 6.0, 6.0, 6.0, 14, 16, 'Loyal, charming, and big-dog attitude', 'Requires regular exercise to maintain physical and mental health', 'Minimal grooming due to short coat; regular brushing helps maintain coat health', 'Prone to certain health issues; regular veterinary check-ups are important', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(9, 'Golden Retriever', 23.0, 24.0, 21.5, 22.5, 65.0, 75.0, 55.0, 65.0, 10, 12, 'Intelligent, Friendly, and Devoted', 'Needs daily activity; enjoys running, retrieving, and canine sports to stay fit and mentally engaged', 'Sheds year-round and seasonally; weekly brushing and occasional baths help manage coat and shedding', 'Generally healthy; monitor for joint, eye, and heart issues. Check ears weekly and brush teeth regularly', 'Requires a balanced diet; monitor portions and limit treats to prevent weight gain', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(10, 'Labrador Retriever', 22.5, 24.5, 21.5, 23.5, 65.0, 80.0, 55.0, 70.0, 11, 13, 'Active, Friendly, and Outgoing', 'Needs plenty of daily exercise; thrives with activities like swimming, retrieving, and canine sports', 'Sheds regularly; occasional baths, nail trims, and frequent teeth brushing keep them clean and healthy', 'Generally healthy; monitor for hip/elbow dysplasia, eye issues, EIC, and bloat symptoms', 'Requires a balanced diet; control portions and treats to prevent obesity', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(11, 'Dachshund', 5.0, 6.0, 5.0, 6.0, 11.0, 11.0, 11.0, 11.0, 12, 16, 'Curious, Friendly, and Spunky', 'Requires regular walks to build muscle and protect the back; avoid stairs and jumping to prevent injury', 'Moderate grooming; coat care varies by type, with regular brushing and monthly nail trims needed', 'Generally healthy; prone to back issues and ear infections—keep weight in check and ears clean', 'Needs a balanced diet with portion control to avoid weight gain and back strain', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(12, 'English Cocker Spaniel', 16.0, 17.0, 15.0, 16.0, 28.0, 34.0, 26.0, 32.0, 12, 14, 'Energetic, merry, and Affectionate', 'Requires regular exercise to maintain physical and mental health', 'Regular grooming to maintain coat health', 'Prone to certain health issues; regular veterinary check-ups are important', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(13, 'English Setter', 25.0, 27.0, 23.0, 25.0, 65.0, 80.0, 45.0, 55.0, 12, 12, 'Friendly, Tolerant, Gentle', 'Needs daily vigorous exercise; avoid high-impact activity for puppies under 2 years', 'Brush weekly, trim face/feet, bathe every 4–6 weeks, and trim nails monthly', 'Generally healthy; watch for hip/elbow dysplasia, deafness, and bloat. Check ears regularly', 'Puppies: 3 small meals/day; adults: 2 meals/day. Monitor weight and prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(14, 'German Shepherd', 24.0, 26.0, 22.0, 24.0, 65.0, 90.0, 50.0, 70.0, 12, 14, 'Courageous, Confident, and Smart', 'Needs daily physical and mental exercise; excels in activities like agility, herding, and tracking', 'Moderate grooming; regular brushing controls shedding, with occasional baths and monthly nail trims', 'Generally healthy; watch for hip/elbow dysplasia and bloat—learn signs and act quickly if needed', 'Requires high-quality food suited to age; avoid fatty scraps and overfeeding to prevent issues', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(15, 'German Shorthaired Pointer', 23.0, 25.0, 21.0, 23.0, 55.0, 70.0, 45.0, 60.0, 10, 12, 'Versatile, enthusiastic, and energetic gundog; thrives on vigorous exercise and positive training; known as the \"perfect pointer\"', 'Requires regular, vigorous exercise to maintain physical and mental health', 'Minimal grooming due to short coat; regular brushing helps maintain coat health', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(16, 'Great Pyrenees', 27.0, 32.0, 25.0, 29.0, 100.0, 100.0, 85.0, 85.0, 10, 12, 'Calm, loyal, and protective dogs with an independent nature', 'Moderate – daily walks or playtime to stay fit', 'Weekly brushing; more often during shedding season', 'Watch for hip dysplasia, bloat, and eye issues', 'Large-breed diet; small frequent meals to prevent bloat', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(17, 'Havanese', 8.5, 11.5, 8.5, 11.5, 7.0, 13.0, 7.0, 13.0, 14, 16, 'Intelligent, Playful, Friendly, Responsive, Gentle', 'Requires daily walks and interactive play; thrives on mental stimulation and companionship. Adaptable to apartment life but needs regular activity to prevent boredom', 'High-maintenance coat requiring daily brushing to prevent matting; regular baths and trims every 6–8 weeks. Eyes and ears need routine cleaning', 'Generally healthy and long-lived; monitor for hereditary conditions like eye disorders and luxating patella. Regular vet checkups are important', 'Benefits from a balanced, high-quality diet suited to small breeds; portion control is key to avoid weight gain. Monitor treats and table food intake', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(18, 'Husky', 21.0, 23.5, 20.0, 22.0, 45.0, 60.0, 35.0, 50.0, 12, 14, 'Loyal, Outgoing, and Mischievous', 'Requires daily exercise and mental stimulation; happiest with a job and must always be leashed or fenced', 'Self-cleaning with minimal odor; weekly brushing and seasonal coat raking keep the coat in good shape', 'Generally healthy and long-lived; low risk of major issues but maintain healthy weight and monitor eyes', 'Needs a high-protein diet adjusted for activity level; avoid overfeeding and monitor weight regularly', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(19, 'Japanese Chin', 8.0, 11.0, 8.0, 11.0, 7.0, 11.0, 7.0, 11.0, 10, 12, 'Affectionate, intelligent, graceful, and cat-like in behavior', 'Requires moderate daily exercise, such as short walks and playtime', 'Regular brushing to maintain coat health and prevent matting', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(20, 'Keeshond', 18.0, 18.0, 17.0, 17.0, 35.0, 45.0, 35.0, 45.0, 12, 15, 'Alert, playful, loyal, affectionate, and intelligent', 'Requires regular daily exercise to maintain physical and mental health', 'Regular brushing needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(21, 'Leonberger', 28.0, 31.5, 25.5, 29.5, 110.0, 170.0, 90.0, 140.0, 7, 7, 'Gentle, patient, family-oriented, and good-natured', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular brushing needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(22, 'Miniature Pinscher', 10.0, 12.5, 10.0, 12.5, 8.0, 10.0, 8.0, 10.0, 12, 16, 'Fearless, energetic, alert, and spirited; known as the \"King of Toys\" for their bold personality and high-stepping gait', 'Requires regular, vigorous exercise to maintain physical and mental health', 'Minimal grooming due to short coat; regular brushing helps maintain coat health', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(23, 'Newfoundland', 28.0, 28.0, 26.0, 26.0, 130.0, 150.0, 100.0, 120.0, 9, 10, 'Sweet, gentle, devoted, and patient; known as \"gentle giants\" and ideal family companions, especially with children', 'Requires moderate daily exercise; enjoys swimming and long walks', 'Weekly brushing and monthly baths to maintain coat health; regular nail trims and dental care', 'Regular veterinary check-ups are important to monitor for potential health issues like hip dysplasia and gastric torsion', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(24, 'Pomeranian', 6.0, 7.0, 6.0, 7.0, 3.0, 7.0, 3.0, 7.0, 12, 16, 'Lively, alert, and extroverted; known for their bold and curious nature', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular brushing needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(25, 'Poodle', 10.0, 15.0, 10.0, 15.0, 10.0, 15.0, 10.0, 15.0, 10, 18, 'Active, Proud, and Very smart; Intelligent, Agile, and Self-confident', 'Very active and energetic; thrives on daily exercise, swimming, retrieving, and long walks', 'Requires frequent brushing and grooming; professional grooming recommended every 4–6 weeks', 'Generally healthy; prone to hip dysplasia, eye disorders, epilepsy, and size-specific orthopedic issues. Standard Poodles are more at risk for bloat', 'Needs a balanced, high-quality diet suited to size and activity level; monitor weight and avoid excessive treats or table scraps', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(26, 'Pug', 10.0, 13.0, 10.0, 13.0, 14.0, 18.0, 14.0, 18.0, 13, 15, 'Charming, affectionate, and sociable; known for their playful and loving nature', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular brushing needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(27, 'Rottweiler', 24.0, 27.0, 22.0, 25.0, 95.0, 135.0, 80.0, 100.0, 9, 10, 'Loyal, Loving, and Confident guardian', 'Athletic and energetic; needs daily physical and mental activity', 'Weekly brushing, regular baths, nail trims, and dental care', 'Generally healthy; watch for hip dysplasia, heart issues, and cancer. Immune support and delayed spay/neuter may help', 'High-quality, life-stage appropriate food; monitor weight and limit treats. Fresh water always available', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(28, 'Saint Bernard', 28.0, 30.0, 26.0, 28.0, 140.0, 180.0, 120.0, 140.0, 8, 10, 'Gentle, patient, and affectionate; known for their calm demeanor and loyalty', 'Requires regular, moderate exercise to maintain health', 'Regular brushing to manage shedding; routine bathing and grooming', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(29, 'Samoyed', 21.0, 23.5, 19.0, 21.0, 45.0, 65.0, 35.0, 50.0, 12, 14, 'Friendly, gentle, and adaptable; known for their \"Sammy smile\" and strong family bonds', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular brushing needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(30, 'Scottish Terrier', 10.0, 10.0, 10.0, 10.0, 19.0, 22.0, 18.0, 21.0, 12, 12, 'Independent, confident, dignified', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular grooming needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(31, 'Shiba Inu', 14.5, 16.5, 13.5, 15.5, 23.0, 23.0, 17.0, 17.0, 13, 16, 'Confident, alert, and good-natured; known for their fox-like appearance and spirited personality', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular brushing needed to manage shedding, especially during seasonal changes', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(32, 'Staffordshire Bull Terrier', 14.0, 16.0, 14.0, 16.0, 28.0, 38.0, 24.0, 34.0, 12, 14, 'Affectionate, courageous, and loyal; known for their \"nanny dog\" reputation due to their gentle nature with children', 'Requires regular, moderate exercise to maintain physical and mental health', 'Minimal grooming needed; regular brushing helps manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(33, 'Wheaten Terrier', 18.0, 19.0, 17.0, 18.0, 35.0, 40.0, 30.0, 35.0, 12, 14, 'Friendly, happy, deeply devoted', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular brushing needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53'),
(34, 'Yorkshire Terrier', 7.0, 8.0, 7.0, 8.0, 7.0, 7.0, 7.0, 7.0, 11, 15, 'Affectionate, sprightly, and tomboyish; known for their small size and big personality', 'Requires regular, moderate exercise to maintain physical and mental health', 'Regular grooming needed to maintain coat health and manage shedding', 'Regular veterinary check-ups are important to monitor for potential health issues', 'Balanced diet essential; monitor food intake to prevent overeating', '2025-06-07 17:35:53', '2025-06-07 17:35:53');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pettypes`
--

CREATE TABLE `pettypes` (
  `pet_type_id` int(11) NOT NULL,
  `pet_type_name` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pettypes`
--

INSERT INTO `pettypes` (`pet_type_id`, `pet_type_name`) VALUES
(2, 'Cat'),
(1, 'Dog');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `catbreeds`
--
ALTER TABLE `catbreeds`
  ADD PRIMARY KEY (`cat_id`),
  ADD UNIQUE KEY `breed_name` (`breed_name`),
  ADD KEY `idx_cat_breed_name` (`breed_name`),
  ADD KEY `idx_cat_life_expectancy` (`life_expectancy_min`,`life_expectancy_max`);

--
-- Indeks untuk tabel `dogbreeds`
--
ALTER TABLE `dogbreeds`
  ADD PRIMARY KEY (`dog_id`),
  ADD UNIQUE KEY `breed_name` (`breed_name`),
  ADD KEY `idx_dog_breed_name` (`breed_name`),
  ADD KEY `idx_dog_life_expectancy` (`life_expectancy_min`,`life_expectancy_max`);

--
-- Indeks untuk tabel `pettypes`
--
ALTER TABLE `pettypes`
  ADD PRIMARY KEY (`pet_type_id`),
  ADD UNIQUE KEY `pet_type_name` (`pet_type_name`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `catbreeds`
--
ALTER TABLE `catbreeds`
  MODIFY `cat_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `dogbreeds`
--
ALTER TABLE `dogbreeds`
  MODIFY `dog_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `pettypes`
--
ALTER TABLE `pettypes`
  MODIFY `pet_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
