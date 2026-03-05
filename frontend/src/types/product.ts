export interface ProductFromListData {
    product_id: number;
    name: string;
    owner_username: string;
    price: number;
    status: string;
    product_photos?: ProductImage[];
}

export interface ProductImage {
    product_photo_id: number;
    image_url: string;
    is_main_photo: boolean;
}

export interface ProductDetailsData {
    product_id: number;
    owner_username: string;
    name: string;
    description: string;
    price: number;
    amount: number;
    color: string;
    weight: number;
    length: number;
    width: number;
    height: number;
    guarantee_period: number;
    status: string;
    product_photos?: ProductImage[];
}
