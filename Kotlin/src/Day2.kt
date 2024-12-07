import java.io.File
import kotlin.math.abs

fun main() {
    val list1 = mutableListOf<Int>()
    val list2 = mutableListOf<Int>()

    File("Kotlin/inputs/day1").forEachLine { line ->
        val values = line.split("\\s+".toRegex())
        list1.add(values[0].toInt())
        list2.add(values[1].toInt())
    }

    fun part1() {
        list1.sort()
        list2.sort()

        val result = list1.zip(list2).sumOf { (a, b) -> abs(a - b) }
        println(result)
    }

    fun part2() {
        val result = list1.sumOf { a -> a * list2.count { it == a } }
        println(result)
    }

    part1()
    part2()
}
