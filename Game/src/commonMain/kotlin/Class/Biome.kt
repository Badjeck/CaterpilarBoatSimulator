// Creation de l'objet Biome
class Biome constructor(val id: Int, val mapId: Int, val isRollable: Boolean, val difficult: Int, val potions: Array<Int> ) {
    init {
        println("Création de la Map - id ${id}")
    }

    fun createMap() {
        println("Bonjour")
    }
}