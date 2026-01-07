-- ==========================================================
-- SCRIPT DE DATOS: CATÁLOGO DE TOURS LIFEXTREME (20+ TOURS)
-- ==========================================================

-- Limpiar tours existentes (opcional, para evitar duplicados si se corre varias veces)
-- DELETE FROM tours; 

INSERT INTO tours (title, slug, description, region, difficulty, duration_days, price_pen, category, images, active, featured) VALUES

-- CUSCO (TREKKING & AVENTURA)
('Choquequirao Trek Clásico', 'choquequirao-4d', 'La hermana sagrada de Machu Picchu. Una caminata exigente sin multitudes hacia la ciudadela perdida.', 'Cusco', 'challenging', 4, 1950.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1526392060635-9d6019884377'], true, true),

('Ausangate 7 Lagunas', 'ausangate-7-lagunas', 'Explora las faldas del nevado Ausangate y sus lagunas turquesas en un día lleno de misticismo andino.', 'Cusco', 'moderate', 1, 350.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1587595431973-160d0d94add1'], true, false),

('Montaña de Colores (Vinicunca)', 'rainbow-mountain-1d', 'El desafío de altura más popular. Conquista los 5,200 msnm y admira los colores de la montaña sagrada.', 'Cusco', 'moderate', 1, 150.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1509216242873-7786f446f465'], true, true),

('Valle Sagrado VIP', 'valle-sagrado-vip', 'Recorrido exclusivo por Pisac, Ollantaytambo y Chinchero. Historia viva y arquitectura inca.', 'Cusco', 'easy', 1, 280.00, 'culture', ARRAY['https://images.unsplash.com/photo-1587595431973-160d0d94add1'], true, false),

('Humantay Lake Challenge', 'humantay-lake', 'Caminata corta pero intensa hacia la laguna esmeralda bajo el glaciar Humantay.', 'Cusco', 'moderate', 1, 180.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1526392060635-9d6019884377'], true, true),

('Huchuy Qosqo Trek', 'huchuy-qosqo-2d', 'Ruta poco conocida por el Balcón del Inca con vistas espectaculares del Valle Sagrado.', 'Cusco', 'moderate', 2, 650.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1587595431973-160d0d94add1'], true, false),

-- HUARAZ (ALPINISMO & ALTA MONTAÑA)
('Laguna 69 Day Hike', 'laguna-69', 'La joya de la Cordillera Blanca. Un ascenso escénico hacia una laguna de azul intenso a 4,600 msnm.', 'Huaraz', 'challenging', 1, 120.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1534234828563-0229dda07976'], true, true),

('Santa Cruz Trek', 'santa-cruz-4d', 'El trekking más famoso de la Cordillera Blanca. Pasos de altura, lagunas y vistas del Alpamayo.', 'Huaraz', 'challenging', 4, 1400.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1464822759023-fed622ff2c3b'], true, true),

('Huayhuash Circuit Full', 'huayhuash-10d', 'Considerado uno de los mejores trekkings alpinos del mundo. 10 días de aislamiento total y belleza extrema.', 'Huaraz', 'extreme', 10, 3500.00, 'expedition', ARRAY['https://images.unsplash.com/photo-1483729558449-99ef09a8c325'], true, true),

('Nevado Mateo Summit', 'nevado-mateo', 'Tu primer 5,000. Ascenso técnico moderado ideal para iniciarse en el montañismo glaciar.', 'Huaraz', 'extreme', 1, 450.00, 'climbing', ARRAY['https://images.unsplash.com/photo-1519681393784-d120267933ba'], true, true),

-- AREQUIPA (CAÑONES & VOLCANES)
('Cañón del Colca Trek 3D', 'colca-canyon-3d', 'Descenso a las profundidades de uno de los cañones más profundos del mundo. Oasis, cóndores y cultura.', 'Arequipa', 'moderate', 3, 480.00, 'trekking', ARRAY['https://images.unsplash.com/photo-1531366936337-7c912a4589a7'], true, true),

('Ascenso Volcán Misti', 'misti-climb-2d', 'Reto vertical. Conquista la cumbre del guardián de Arequipa a 5,822 msnm. Solo para valientes.', 'Arequipa', 'extreme', 2, 850.00, 'climbing', ARRAY['https://images.unsplash.com/photo-1605540436563-5bca919ae763'], true, false),

('Ruta del Sillar & Canteras', 'ruta-sillar', 'Recorrido cultural por las canteras donde nace la arquitectura de la Ciudad Blanca.', 'Arequipa', 'easy', 1, 90.00, 'culture', ARRAY['https://images.unsplash.com/photo-1531366936337-7c912a4589a7'], true, false),

-- SELVA (AMAZONAS)
('Tambopata Jungle Adventure', 'tambopata-4d', 'Expedición a la Reserva Nacional. Avistamiento de guacamayos, caimanes y caminatas nocturnas.', 'Madre de Dios', 'moderate', 4, 1800.00, 'jungle', ARRAY['https://images.unsplash.com/photo-1581881067989-713d26a5c8d2'], true, true),

('Manu Biosphere Reserve', 'manu-6d', 'Inmersión profunda en la zona reservada del Manu. La mayor biodiversidad del planeta.', 'Madre de Dios', 'challenging', 6, 3200.00, 'expedition', ARRAY['https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f'], true, false),

('Iquitos Amazonas Cruise', 'iquitos-cruise-3d', 'Navegación de lujo por el río Amazonas. Delfines rosados, tribus locales y atardeceres mágicos.', 'Iquitos', 'easy', 3, 2500.00, 'cruise', ARRAY['https://images.unsplash.com/photo-1580619305218-8423a7ef79b4'], true, true),

-- ICA & COSTA
('Islas Ballestas & Paracas', 'paracas-full-day', 'Fauna marina, candelabro y reserva nacional. El "Galápagos de los pobres".', 'Ica', 'easy', 1, 150.00, 'nature', ARRAY['https://images.unsplash.com/photo-1589553416260-f586c8f1514f'], true, false),

('Nazca Lines Flight', 'nazca-flight', 'Sobrevuelo a las enigmáticas líneas de Nazca. Un misterio arqueológico desde el aire.', 'Ica', 'easy', 1, 400.00, 'flight', ARRAY['https://images.unsplash.com/photo-1531219432768-9f540ce91ef3'], true, true),

('Lunahuaná Rafting & Canopy', 'lunahuana-full-day', 'Aventura cerca de Lima. Canotaje en el río Cañete, vinos y adrenalina.', 'Lima', 'easy', 1, 180.00, 'adventure', ARRAY['https://images.unsplash.com/photo-1530866495561-507c9faab2ed'], true, false);

-- Verificar inserción
SELECT count(*) as total_tours FROM tours;
SELECT title, region, price_pen FROM tours ORDER BY created_at DESC LIMIT 5;
