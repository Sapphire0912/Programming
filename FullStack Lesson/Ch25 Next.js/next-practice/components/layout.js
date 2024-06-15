import Head from "next/head";
import Link from "next/link";
import styles from "./layout.module.css";

const name = "Sapphire";
const webTitle = "Next.js 練習網站";

export default function Layout({ children, returnBack }) {
  return (
    <div className={styles.layout}>
      <Head>
        <meta name="author" content="Sapphire" />
        <meta charSet="utf-8"></meta>
        <meta name="viewport" content="width=device-width,initial-scale=1" />
      </Head>
      <header className={styles.header}>
        <h1>{webTitle}</h1>
        <h2>{name}</h2>
      </header>
      <main>{children}</main>
      {returnBack && (
        <Link className={styles.home} href="/">
          回到首頁
        </Link>
      )}
    </div>
  );
}
