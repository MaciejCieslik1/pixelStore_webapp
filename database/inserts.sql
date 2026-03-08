INSERT INTO user (email, username, password, is_verified, bio, money) VALUES
    ('salesman1@gmail.com', 'exemplary_salesman1', '123456789', 1,
     'I am an exemplary salesman', 1000000);

INSERT INTO user_statistics (user_id, creation_date, products_bought, products_sold) VALUES
    (1, "2026-01-01", 0, 0);


INSERT INTO product (owner_id, name, description, price, amount, color, weight, length, width, height, guarantee_period, status) VALUES
    (1, 'intel core I7 14700K', 'powerful gaming cpu', 1500, 3, 'silver', 0.05, 5, 8,
     0.5, 5.0, 'available'),
    (1, 'ATX gaming motherboard Z790', 'atx motherboard for gamers', 1000, 3, 'silver', 0.05, 50, 35,
     0.05, 5.0, 'available'),
    (1, 'nvidia geforce rtx 4060', 'powerful gaming gpu', 2500, 2, 'black', 1.25, 30, 10,
     7, 3.0, 'available'),
    (1, 'SSD NVME 1TB ', 'large and fast disk', 500, 10, 'black', 0.1, 10, 3,
     0.1, 4.0, 'available'),
    (1, 'power supply unit 750W Plus gold', 'safe and quit PSU', 800, 2, 'grey', 2.5, 0.25, 15,
     10, 9.0, 'available');


INSERT INTO category (name, description) VALUES
    ('Processors', 'Central processing units (CPUs) for desktops and laptops'),
    ('Graphics Cards', 'Cards responsible for rendering graphics and 3D images'),
    ('Motherboards', 'Main circuit boards connecting all computer components'),
    ('RAM', 'Memory modules of various capacities and speeds'),
    ('SSD Drives', 'Fast solid-state drives for data storage'),
    ('HDD Drives', 'Traditional spinning hard disk drives with large capacity'),
    ('Power Supplies', 'Devices providing stable power to all components'),
    ('Cases', 'Chassis protecting and housing computer components'),
    ('Cooling Systems', 'Fans, liquid cooling, and other heat dissipation solutions'),
    ('Optical Drives', 'CD/DVD/Blu-ray drives for reading and writing optical discs'),
    ('Other', 'other stuff');


INSERT INTO category_product (category_id, product_id) VALUES
    (1, 1),
    (3, 2),
    (2, 3),
    (5, 4),
    (7, 5);


INSERT INTO product_photo (product_id, image_url, is_main_photo) VALUES
    (1, 'https://images.pexels.com/photos/1010487/pexels-photo-1010487.jpeg',
     TRUE),
    (1, 'https://images.pexels.com/photos/40879/cpu-processor-macro-pen-40879.jpeg', FALSE),

    (2, 'https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg', TRUE),
    (2, 'https://images.pexels.com/photos/2582932/pexels-photo-2582932.jpeg', FALSE),

    (3, 'https://images.pexels.com/photos/6704948/pexels-photo-6704948.jpeg', TRUE),
    (3, 'https://images.pexels.com/photos/6704939/pexels-photo-6704939.jpeg', FALSE),

    (4, 'https://images.pexels.com/photos/28666524/pexels-photo-28666524.jpeg',
     TRUE),
    (4, 'https://images.pexels.com/photos/5222605/pexels-photo-5222605.jpeg',
     FALSE),

    (5, 'https://images.pexels.com/photos/33173003/pexels-photo-33173003.jpeg', TRUE),
    (5, 'https://images.pexels.com/photos/33174696/pexels-photo-33174696.jpeg', FALSE);
