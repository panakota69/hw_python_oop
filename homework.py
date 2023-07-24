from dataclasses import dataclass, asdict
from typing import Union


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    KMH_IN_MS: float = 0.278
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    WEIGHT_COEFF_1: float = 0.035
    WEIGHT_COEFF_2: float = 0.029
    HEIGHT_IN_M: int = 100
    KMH_IN_MS: float = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed() * self.KMH_IN_MS
        return (((self.WEIGHT_COEFF_1 * self.weight + (mean_speed**2
                / self.height * self.HEIGHT_IN_M) * self.WEIGHT_COEFF_2
                * self.weight) * self.duration * self.MIN_IN_H))


class Swimming(Training):
    LEN_STEP: float = 1.38
    SWIMMING_MEAN_SPEED_MULTIPLIER: int = 2
    SWIMMING_MEAN_SPEED_SHIFT: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWIMMING_MEAN_SPEED_SHIFT)
                * self.SWIMMING_MEAN_SPEED_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[Union[int, float]]) -> Training:
    training_types: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type not in training_types:
        raise KeyError(f'{workout_type}: Такой тренировки нет!')
    else:
        train: Training = training_types[workout_type](*data)
        return train


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training is not None:
            main(training)
