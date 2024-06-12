import Link from "next/link";

export default function Home() {
  return (
    <div>
      <h1>這是網站首頁.</h1>
      {/* <a href="/posts/edit-post">編輯 post</a> */}
      <Link href="/posts/edit-post">編輯 post</Link>
    </div>
  );
}
