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
