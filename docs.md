export interface Blog {
  id: string;
  title: string;
  slug: string;
  content: string;
  thumbnail: string;
  published: boolean;
  created_at: string;
  updated_at: string;
  tags: string[];
  series_id?: string;
  likes: number;
}

export interface Series {
  id: string;
  title: string;
  slug: string;
  description: string;
  blogs: Blog[];
}

export interface Comment {
  id: string;
  blog_id: string;
  username: string;
  comment: string;
  created_at: string;
}

export interface User {
  id: string;
  isAdmin: boolean;
}
