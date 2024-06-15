import Layout from "../components/layout";
import Link from "next/link";

export default function newPage() {
  return (
    <Layout returnBack={true}>
      <h2>This is a new Page.</h2>
    </Layout>
  );
}
