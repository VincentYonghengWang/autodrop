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

