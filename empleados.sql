-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-04-2025 a las 01:58:34
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `empleados`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `id_administrador` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `contraseña` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id_administrador`, `usuario`, `contraseña`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia`
--

CREATE TABLE `asistencia` (
  `id_asistencia` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_entrada` time DEFAULT NULL,
  `hora_salida` time DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asistencia`
--

INSERT INTO `asistencia` (`id_asistencia`, `fecha`, `hora_entrada`, `hora_salida`, `id_empleado`) VALUES
(1, '2025-04-08', '08:00:00', '16:00:00', 1),
(2, '2025-04-09', '09:00:00', '17:00:00', 2),
(3, '2025-04-10', '07:45:00', '15:45:00', 3),
(4, '2025-04-11', '10:15:00', '18:30:00', 4),
(5, '2025-04-14', '06:00:00', '14:00:00', 5),
(6, '2025-04-15', '13:10:00', '21:00:00', 6),
(7, '2025-04-16', '14:00:00', '22:00:00', 7),
(8, '2025-04-17', '15:00:00', '23:00:00', 8),
(9, '2025-04-18', '12:00:00', '20:00:00', 9),
(10, '2025-04-21', '11:30:00', '19:30:00', 10),
(11, '2025-04-23', '11:25:02', '11:26:00', 2),
(12, '2025-04-23', '11:25:28', '11:26:21', 1),
(13, '2025-04-23', '11:39:29', '11:39:31', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `id_empleado` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `puesto` varchar(100) DEFAULT NULL,
  `rfc` varchar(13) DEFAULT NULL,
  `fecha_nac` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`id_empleado`, `nombre`, `apellido`, `correo`, `telefono`, `puesto`, `rfc`, `fecha_nac`) VALUES
(1, 'miguel', 'martinez', 'miguel@gmail.com', '2386812361623', 'gerente', '3fh23f23hf123', '1999-04-02'),
(2, 'Carlos Alberto', 'Ramírez González', 'carlos.alberto.ramirez@email.com', '5534567890', 'Analista de Datos', 'RARC950101ABC', '1995-01-01'),
(3, 'María Fernanda', 'González Pérez', 'maria.fernanda.gonzalez@email.com', '5543219876', 'Diseñadora UX', 'GOMR970202DEF', '1997-02-02'),
(4, 'José Antonio', 'Hernández López', 'jose.antonio.hernandez@email.com', '5523456789', 'Programador Jr.', 'HEJJ960303GHI', '1996-03-03'),
(5, 'Ana María', 'López Rodríguez', 'ana.maria.lopez@email.com', '5567891234', 'Recursos Humanos', 'LOPA980404JKL', '1998-04-04'),
(6, 'Luis Fernando', 'Martínez Sánchez', 'luis.fernando.martinez@email.com', '5578912345', 'Soporte Técnico', 'MALU990505MNO', '1999-05-05'),
(7, 'Sofía Carolina', 'Pérez Jiménez', 'sofia.carolina.perez@email.com', '5589123456', 'Administradora', 'PESO000606PQR', '2000-06-06'),
(8, 'Miguel Ángel', 'Torres Cruz', 'miguel.angel.torres@email.com', '5591234567', 'Contador', 'TOMI940707STU', '1994-07-07'),
(9, 'Fernanda Isabel', 'Sánchez García', 'fernanda.isabel.sanchez@email.com', '5512345678', 'Ingeniera Industrial', 'SAFE930808VWX', '1993-08-08'),
(10, 'Jorge Luis', 'Cruz Martínez', 'jorge.luis.cruz@email.com', '5523987654', 'Marketing Digital', 'CRJO990909YZA', '1999-09-09'),
(11, 'Daniela Sofía', 'Morales Gómez', 'daniela.sofia.morales@email.com', '5539876543', 'Diseñadora Gráfica', 'MODA000101BCD', '2000-01-01'),
(12, 'pablo tercero', 'pineda cruz', 'pablo.cruz@gmail.com', '9965340892', 'contabilidad', 'VECJ880326XXX', '1997-04-09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE `horario` (
  `id_horario` int(11) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `dias_laborables` int(11) NOT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horario`
--

INSERT INTO `horario` (`id_horario`, `hora_inicio`, `hora_fin`, `dias_laborables`, `id_empleado`) VALUES
(1, '08:00:00', '16:00:00', 5, 1),
(2, '09:00:00', '17:00:00', 5, 2),
(3, '07:30:00', '15:30:00', 5, 3),
(4, '10:00:00', '18:00:00', 5, 4),
(5, '06:00:00', '14:00:00', 5, 5),
(6, '13:00:00', '21:00:00', 5, 6),
(7, '14:00:00', '22:00:00', 5, 7),
(8, '15:00:00', '23:00:00', 5, 8),
(9, '12:00:00', '20:00:00', 5, 9),
(10, '11:00:00', '19:00:00', 5, 10),
(11, '06:00:00', '16:00:00', 5, 11),
(12, '05:00:00', '12:00:00', 4, 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nomina`
--

CREATE TABLE `nomina` (
  `id_nomina` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `sueldo_por_hora` float DEFAULT NULL,
  `horas` float DEFAULT NULL,
  `total_pago` float DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `nomina`
--

INSERT INTO `nomina` (`id_nomina`, `fecha`, `sueldo_por_hora`, `horas`, `total_pago`, `id_empleado`) VALUES
(1, '2025-04-08', 85.5, 40, 3420, 1),
(2, '2025-04-09', 90, 35, 3150, 2),
(3, '2025-04-10', 88.75, NULL, 710, 3),
(4, '2025-04-11', 95, 32, 3040, 4),
(5, '2025-04-14', 100, NULL, 800, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `pin` int(11) NOT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `pin`, `id_empleado`) VALUES
(1, 1234, 1),
(2, 5678, 2),
(3, 9101, 3),
(4, 1122, 4),
(5, 3344, 5),
(6, 5566, 6),
(7, 7788, 7),
(8, 9900, 8),
(9, 1234, 9),
(10, 5678, 10);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id_administrador`);

--
-- Indices de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD PRIMARY KEY (`id_asistencia`),
  ADD KEY `id_empleado` (`id_empleado`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`id_empleado`),
  ADD UNIQUE KEY `Correo` (`correo`),
  ADD UNIQUE KEY `Rfc` (`rfc`);

--
-- Indices de la tabla `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`id_horario`),
  ADD KEY `id_empleado` (`id_empleado`);

--
-- Indices de la tabla `nomina`
--
ALTER TABLE `nomina`
  ADD PRIMARY KEY (`id_nomina`),
  ADD KEY `id_empleado` (`id_empleado`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `id_empleado` (`id_empleado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id_administrador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  MODIFY `id_asistencia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `id_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `id_horario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `nomina`
--
ALTER TABLE `nomina`
  MODIFY `id_nomina` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD CONSTRAINT `asistencia_ibfk_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id_empleado`);

--
-- Filtros para la tabla `horario`
--
ALTER TABLE `horario`
  ADD CONSTRAINT `horario_ibfk_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id_empleado`);

--
-- Filtros para la tabla `nomina`
--
ALTER TABLE `nomina`
  ADD CONSTRAINT `nomina_ibfk_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id_empleado`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id_empleado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
