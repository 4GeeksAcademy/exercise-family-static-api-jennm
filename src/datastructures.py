"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

        # Inicializar la familia con los 3 miembros especificados
        self.add_member({
            "first_name": "John",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        })
        self.add_member({
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        })
        self.add_member({
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        })

    # Genera un ID único para cada miembro (no modificar)
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        """
        Agrega un nuevo miembro a la familia.
        Si no viene con 'id', se asigna uno automáticamente.
        Se agrega siempre 'last_name' con el apellido de la familia.
        """
        if "id" not in member:
            member["id"] = self._generate_id()
        else:
            # Si el cliente envió un id, actualizar _next_id si es necesario para evitar duplicados
            if member["id"] >= self._next_id:
                self._next_id = member["id"] + 1

        # Añadir el apellido fijo "Jackson"
        member["last_name"] = self.last_name

        self._members.append(member)
        return member  # Retornar el miembro agregado

    def delete_member(self, id):
        """
        Elimina un miembro por su ID.
        """
        for i, member in enumerate(self._members):
            if member["id"] == id:
                self._members.pop(i)
                return True  # Eliminado con éxito
        return False  # No encontrado

    def get_member(self, id):
        """
        Obtiene un miembro por su ID.
        """
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        """
        Devuelve la lista completa de miembros.
        """
        return self._members
