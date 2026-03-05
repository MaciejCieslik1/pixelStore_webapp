export interface ProductFromListData {
    product_id: number;
    name: string;
    sellerUsername: string;
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
    sellerUsername: string;
    name: string;
    description: string;
    price: number;
    amount: number;
    color: string;
    weight: number;
    length: number;
    height: number;
    guarantee_period: number;
    status: string;
    product_photos?: ProductImage[];
}
