export type MetricCard = {
  title: string;
  value: string;
  delta: string;
  tone: string;
};

export type PipelineStage = {
  name: string;
  count: number;
  detail: string;
};

export type ProductRow = {
  id: number;
  product_name: string;
  source: string;
  margin: number;
  status: string;
  channels: string[];
  factory_hint: { city?: string; category?: string; factory_count?: number } | null;
  created_at: string;
};

export type ActivityItem = {
  robot_name: string;
  message: string;
  status: string;
  created_at: string;
};

export type ExceptionItem = {
  id: number;
  type: string;
  description: string;
  status: string;
  severity: string;
  created_at: string;
};

export type DashboardResponse = {
  metrics: MetricCard[];
  pipeline: PipelineStage[];
  products: ProductRow[];
  activity: ActivityItem[];
  exceptions: ExceptionItem[];
};

export type StorefrontProduct = {
  id: number;
  product_name: string;
  source: string;
  status: string;
  price: number;
  compare_at_price: number | null;
  margin: number;
  channels: string[];
  factory_hint: { city?: string; category?: string; factory_count?: number } | null;
  badge: string;
  subtitle: string;
  image_tone: string;
};

export type StorefrontResponse = {
  products: StorefrontProduct[];
  hero_product: StorefrontProduct | null;
  total_products: number;
  updated_label: string;
};

export type CheckoutResponse = {
  order_id: number;
  product_name: string;
  revenue: number;
  supplier: string;
  tracking_number: string | null;
  status: string;
};
