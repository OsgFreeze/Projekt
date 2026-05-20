import Link from "next/link"

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link href="/" className="navLink">
        Home
      </Link>
    </nav>
  )
}