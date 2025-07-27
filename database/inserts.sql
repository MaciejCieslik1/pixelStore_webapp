INSERT INTO user (email, username, password_hash, is_verified, bio, money) VALUES
    ('salesman1@gmail.com', 'exemplary_salesman1', '123456789', 1,
     'I am an exemplary salesman', 1000000);


INSERT INTO product (owner_id, name, description, price, amount, color, weight, length, width, height, guarantee_period) VALUES
    (1, 'intel core I7 14700K', 'powerful gaming cpu', 1500, 3, 'silver', 0.05, 5, 8,
     0.5, 5.0),
    (1, 'ATX gaming motherboard Z790', 'atx motherboard for gamers', 1000, 3, 'silver', 0.05, 50, 35,
     0.05, 5.0),
    (1, 'nvidia geforce rtx 4060', 'powerful gaming gpu', 2500, 2, 'black', 1.25, 30, 10,
     7, 3.0),
    (1, 'SSD NVME 1TB ', 'large and fast disk', 500, 10, 'black', 0.1, 10, 3,
     0.1, 4.0),
    (1, 'power supply unit 750W Plus gold', 'safe and quit PSU', 800, 2, 'grey', 2.5, 0.25, 15,
     10, 9.0);


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
    (1, 'https://www.pexels.com/pl-pl/zdjecie/stos-komputerowych-jednostek-przetwarzania-1010487/',
     TRUE),
    (1, 'https://www.pexels.com/pl-pl/zdjecie/brazowo-zielony-procesor-komputerowy-40879/', FALSE),

    (2, 'https://www.pexels.com/pl-pl/zdjecie/plyta-glowna-czarno-szara-2582937/', TRUE),
    (2, 'https://www.pexels.com/pl-pl/zdjecie/plyta-glowna-czarno-szara-2582932/', FALSE),

    (3, 'https://www.pexels.com/pl-pl/zdjecie/czarno-bialy-metal-metalowy-technologia-6704948/', TRUE),
    (3, 'https://www.pexels.com/pl-pl/zdjecie/metal-metalowy-odbicie-fan-6704939/', FALSE),

    (4, 'https://www.pexels.com/pl-pl/zdjecie/wysokowydajny-dysk-ssd-nvme-na-szarej-powierzchni-28666524/',
     TRUE),
    (4, 'https://www.pexels.com/pl-pl/zdjecie/seagate-ssd-sprzet-komputerowy-dysk-ssd-5222605/',
     FALSE),

    (5, 'https://www.pexels.com/pl-pl/zdjecie/czarny-zasilacz-na-bialym-tle-33173003/', TRUE),
    (5, 'https://www.pexels.com/pl-pl/zdjecie/wysokowydajny-zasilacz-do-gier-33174696/', FALSE);
