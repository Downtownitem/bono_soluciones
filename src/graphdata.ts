export interface PlotsData {
    x_vals: number[];
    y_original: number[];
    y_taylor: number[];
}

export interface ScattersData {
    x_val: number;
    f_lambdified: number;
    taylor_lambdified: number;
}

export interface Graphics {
    plots: PlotsData;
    scatters: ScattersData;
}

export interface GraphData {
    error: boolean;
    generated_polinomy: string;
    teoric_value: number;
    experimental_value: number;
    absolute_error: number;
    relative_error: number;
    plots: Graphics;
}